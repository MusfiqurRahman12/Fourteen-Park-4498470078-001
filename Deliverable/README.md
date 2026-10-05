# Fourteen Park | Amenities & Lifestyle Eblast
### Project ID: `4498470078-001` (Kolter Urban / Ansley Real Estate)

---

## 📦 Deliverable Package Overview

This deliverable package contains production-ready, dark-mode-hardened HTML email templates and assets for the **Fourteen Park Amenities & Lifestyle Eblast**.

```
Deliverable/
├── index.html               # Production HTML template (relative "images/" paths)
├── index-hosted.html        # Standalone HTML template (uses high-speed Cloudflare CDN image URLs)
├── mailchimp-template.html  # Mailchimp master template (mc:edit regions + CAN-SPAM merge tags)
├── README.md                # Documentation & ESP deployment guide
├── images/
│   ├── hero-banner.jpg      # Header rendering + Fourteen Park logo at dusk (650x574)
│   ├── cta-button.png       # "JOIN THE INTEREST LIST" CTA button box (811x212 @ 1.25x)
│   └── footer-bottom.png    # Logo, legal disclaimer & partner logos (811x672 @ 1.25x)
└── previews/
    ├── preview-desktop.png  # Full-length 650px desktop render
    └── preview-mobile.png   # Fluid 390px mobile viewport render
```

---

## 🚀 Which File Should I Use?

| File | Best Used For | Notes |
| :--- | :--- | :--- |
| **`index-hosted.html`** | **Direct Sending & Fast Import** | Self-contained, single-file HTML. All images load directly from global Cloudflare CDN endpoints. Works immediately in any ESP or CRM (HubSpot, Salesforce, Klaviyo, SendGrid, etc.). |
| **`mailchimp-template.html`** | **Mailchimp Campaigns** | Includes Mailchimp `mc:edit` editable content blocks, zero-height preheader tags, and CAN-SPAM compliant unsubscribe/preference merge tags. |
| **`index.html`** | **Self-Hosted / ZIP Upload** | References `./images/`. Upload the `images/` folder alongside `index.html` to your own media server, FTP, or zip-based ESP importer. |

---

## 🌐 Hosted Image Endpoints (Cloudflare CDN)

All assets are pre-hosted on high-speed, persistent global CDN endpoints with permanent cache headers:

- **Hero Banner**: `https://iili.io/n03T7mg.jpg`
- **CTA Button**: `https://iili.io/n12Rbyb.png`
- **Bottom Footer & Logos**: `https://iili.io/n125JnV.png`

---

## 🛡️ Dark Mode & Client Hardening Specifications

1. **iOS / Apple Mail**:
   - Uses `color-scheme: light only` and `-webkit-text-fill-color` locks.
   - Prevents iOS WebKit from inverting the dark text into white on the cream panel.
2. **Gmail App (iOS & Android)**:
   - All critical bottom elements (CTA button, Fourteen Park branding, legal disclaimers, and partner logos) are pre-rendered into high-density assets sharing the exact `#3F342A` brand brown.
   - Both bottom images are wrapped in destination links (`https://FourteeenPark.com`), preventing Gmail Desktop from showing hover "Download" button overlays.
3. **Outlook Desktop (Windows Word Engine)**:
   - Uses 650px MSO ghost tables (`<!--[if mso]>`).
   - Bulletproof table cell styling ensures zero layout collapse across Outlook 2016, 2019, and Microsoft 365.
4. **Anti-Gap Body Rule**:
   - `<body>` is styled with `font-size: 0; line-height: 0;` to collapse any empty line boxes introduced by ESP tracking pixels at the bottom of the email.

---

## 🔗 Destination URLs

- **Primary Destination**: `https://FourteeenPark.com`
- **CTA Action**: "Join The Interest List" opens `https://FourteeenPark.com` in a new browser tab (`target="_blank"`).
