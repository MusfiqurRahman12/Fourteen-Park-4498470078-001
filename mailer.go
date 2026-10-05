package main

import (
	"context"
	"fmt"
	"os"

	"github.com/mailtrap/mailtrap-go"
)

// Mailer wraps the Mailtrap client and configuration
type Mailer struct {
	client *mailtrap.Client
	cfg    *Config
}

// NewMailer initializes a Mailtrap client according to the active configuration
func NewMailer(cfg *Config) (*Mailer, error) {
	if cfg.APIToken == "" {
		return nil, fmt.Errorf("missing Mailtrap API token: please set MAILTRAP_API_TOKEN in .env or environment")
	}

	var opts []mailtrap.Option
	if cfg.UseSandbox && cfg.InboxID > 0 {
		opts = append(opts, mailtrap.WithSandbox(true), mailtrap.WithSandboxID(cfg.InboxID))
	}

	client, err := mailtrap.NewClient(cfg.APIToken, opts...)
	if err != nil {
		return nil, fmt.Errorf("failed to initialize Mailtrap client: %w", err)
	}

	return &Mailer{
		client: client,
		cfg:    cfg,
	}, nil
}

// SendMessage sends an email using the Mailtrap API
func (m *Mailer) SendMessage(ctx context.Context, req *mailtrap.SendRequest) (*mailtrap.SendResponse, error) {
	// Fall back to default From address if not populated
	if req.From.Email == "" {
		req.From = mailtrap.Address{
			Email: m.cfg.SenderEmail,
			Name:  m.cfg.SenderName,
		}
	}

	resp, _, err := m.client.Send(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("mailtrap send failed: %w", err)
	}

	return resp, nil
}

// SendFromTemplate sends an email using a hosted Mailtrap Email Template UUID
func (m *Mailer) SendFromTemplate(ctx context.Context, templateUUID string, templateVars map[string]any, toEmail, toName string) (*mailtrap.SendResponse, error) {
	req := &mailtrap.SendRequest{
		From: mailtrap.Address{
			Email: m.cfg.SenderEmail,
			Name:  m.cfg.SenderName,
		},
		To: []mailtrap.Address{
			{
				Email: toEmail,
				Name:  toName,
			},
		},
		TemplateUUID:      templateUUID,
		TemplateVariables: templateVars,
	}

	return m.SendMessage(ctx, req)
}

// SendEblast sends the Fourteen Park HTML email template from index.html
func (m *Mailer) SendEblast(ctx context.Context, toEmail, toName string) (*mailtrap.SendResponse, error) {
	htmlBytes, err := os.ReadFile("index.html")
	if err != nil {
		return nil, fmt.Errorf("failed to read index.html: %w", err)
	}

	req := &mailtrap.SendRequest{
		From: mailtrap.Address{
			Email: m.cfg.SenderEmail,
			Name:  m.cfg.SenderName,
		},
		To: []mailtrap.Address{
			{
				Email: toEmail,
				Name:  toName,
			},
		},
		Subject:  "Fourteen Park | Amenities & Lifestyle Eblast",
		Text:     "Fourteen Park is thoughtfully designed around a curated collection of amenities that elevate everyday living.",
		HTML:     string(htmlBytes),
		Category: "Fourteen Park Eblast",
	}

	return m.SendMessage(ctx, req)
}
