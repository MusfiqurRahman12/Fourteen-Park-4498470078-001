package main

import (
	"context"
	"fmt"
	"log"
)

func main() {
	// 1. Load configuration from .env and environment variables
	cfg := LoadConfig()

	// 2. Initialize Mailer service
	mailer, err := NewMailer(cfg)
	if err != nil {
		log.Fatalf("Initialization error: %v", err)
	}

	// 3. Send using the Mailtrap Hosted Email Template
	fmt.Printf("Sending test email using Template UUID: %s...\n", cfg.TemplateUUID)
	resp, err := mailer.SendFromTemplate(
		context.Background(),
		cfg.TemplateUUID,
		map[string]any{
			"user_name": cfg.RecipientName,
		},
		cfg.RecipientEmail,
		cfg.RecipientName,
	)
	if err != nil {
		log.Fatalf("Template send error: %v", err)
	}

	// 4. Output response message IDs
	fmt.Printf("Email sent successfully using Template! Message IDs: %v\n", resp.MessageIDs)

	if cfg.UseSandbox {
		fmt.Printf("Sandbox Inbox URL: https://mailtrap.io/inboxes/%d\n", cfg.InboxID)
	} else {
		fmt.Println("Check sent logs at: https://mailtrap.io/sending/email_logs")
	}
}
