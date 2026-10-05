package main

import (
	"log"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

// Config holds the email service configuration loaded from environment variables / .env
type Config struct {
	APIToken       string
	InboxID        int64
	UseSandbox     bool
	SenderEmail    string
	SenderName     string
	RecipientEmail string
	RecipientName  string
	TemplateUUID   string
}

// LoadConfig reads configuration from .env and environment variables.
func LoadConfig() *Config {
	// Attempt to load .env if present (non-fatal if missing)
	_ = godotenv.Load()

	apiToken := os.Getenv("MAILTRAP_API_TOKEN")
	if apiToken == "" {
		log.Println("WARNING: MAILTRAP_API_TOKEN is not set in environment or .env file")
	}

	inboxIDStr := os.Getenv("MAILTRAP_INBOX_ID")
	var inboxID int64
	if inboxIDStr != "" {
		if id, err := strconv.ParseInt(inboxIDStr, 10, 64); err == nil {
			inboxID = id
		}
	}

	useSandbox := true
	if val := os.Getenv("MAILTRAP_USE_SANDBOX"); val == "false" || val == "0" {
		useSandbox = false
	}

	senderEmail := os.Getenv("MAILTRAP_SENDER_EMAIL")
	if senderEmail == "" {
		// Use Mailtrap's demo domain default for testing, or your verified domain
		senderEmail = "hello@demomailtrap.co"
	}

	senderName := os.Getenv("MAILTRAP_SENDER_NAME")
	if senderName == "" {
		senderName = "Fourteen Park"
	}

	recipientEmail := os.Getenv("MAILTRAP_RECIPIENT_EMAIL")
	if recipientEmail == "" {
		recipientEmail = "gravityahmed11@gmail.com"
	}

	recipientName := os.Getenv("MAILTRAP_RECIPIENT_NAME")
	if recipientName == "" {
		recipientName = "Ahmed"
	}

	templateUUID := os.Getenv("MAILTRAP_TEMPLATE_UUID")
	if templateUUID == "" {
		templateUUID = "fdf909bd-bb39-4d8d-9a24-258309475d99"
	}

	return &Config{
		APIToken:       apiToken,
		InboxID:        inboxID,
		UseSandbox:     useSandbox,
		SenderEmail:    senderEmail,
		SenderName:     senderName,
		RecipientEmail: recipientEmail,
		RecipientName:  recipientName,
		TemplateUUID:   templateUUID,
	}
}
