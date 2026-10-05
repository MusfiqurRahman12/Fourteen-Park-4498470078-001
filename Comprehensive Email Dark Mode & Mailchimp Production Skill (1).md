---
name: bulletproof-email-darkmode-mailchimp
description: Enterprise skill for generating and refactoring HTML email templates with zero background-color vs. image seams across iOS Mail, Gmail, Outlook, and Mailchimp.
version: 3.0.0
target_environment: Antigravity Agent Engine (Model 3.8.7.9+ / Cloud)
supported_esp: Mailchimp
supported_clients:
  - Apple Mail (iOS / macOS)
  - Gmail App (iOS / Android)
  - Outlook (Desktop MSO 2016-365, iOS, Android, Web/OWA)
triggers:
  - "email blast"
  - "e-blast"
  - "html email"
  - "dark mode"
  - "gmail dark mode"
  - "outlook dark mode"
  - "mailchimp template"
  - "vml button"
  - "image seam"
---

# Bulletproof Email Dark Mode & Mailchimp Automation Skill

## 1. Engine Rendering & Inversion Matrix

| Client / Platform | Engine Type | Dark Mode Behavior | Defense Mechanism |
| :--- | :--- | :--- | :--- |
| **Apple Mail (iOS / macOS)** | WebKit | Dynamic hex recalculation | `linear-gradient(#HEX, #HEX)` + `color-scheme: light dark` |
| **Outlook Mobile & Web (OWA)** | WebKit / Blink | Injects `[data-ogsc]` / `[data-ogsb]` | Attribute selectors with `!important` |
| **Outlook Desktop (Windows)** | Microsoft Word (MSO) | High-contrast inversion | VML (`v:roundrect`), HTML `bgcolor`, `mso-hide: all;` |
| **Gmail App (iOS / Android)** | WebKit / Blink | Heuristic color inversion (strips media queries) | Off-hex values (`#FFFFFE`), transparent PNGs with halos, inline styling |
| **Mailchimp ESP** | Inliner Engine | Converts `<style>` to inline attributes | Protects non-inlinable media queries and keeps `mc:edit` off styled `<td>` elements |

---

## 2. Mailchimp Integration Directives

1. **Inliner Safeguards**:
   - Mailchimp's automated CSS inliner flattens baseline styles into inline `style=""` declarations.
   - Non-inlinable rules (`@media (prefers-color-scheme: dark)` and `[data-ogsc]`) must stay strictly in the `<head>` `<style type="text/css">` block.
   - Every `<td>` and `<table>` must include an inline `bgcolor=""` alongside `background-color` and `linear-gradient` to prevent stripped styles during campaign compilation.

2. **Tag Isolation (`mc:edit` & `mc:repeatable`)**:
   - **Never** place `mc:edit` directly on structural `<td>` elements that carry color-locking gradients or padding. Mailchimp's visual builder can rewrite the element's style attribute.
   - Always place `mc:edit` on inner child elements (e.g., `<div mc:edit="body_content">` or `<span mc:edit="btn_text">`).

3. **Required Mailchimp Merge Tags**:
   Every commercial e-blast must include Mailchimp's CAN-SPAM and compliance tags styled defensively so they do not produce unreadable contrast in dark mode:
   - `*|UNSUB|*`: Unsubscribe link URL
   - `*|UPDATE_PROFILE|*`: Preferences update URL
   - `*|LIST:ADDRESSLINE|*`: Physical address
   - `*|CURRENT_YEAR|*` and `*|LIST:COMPANY|*`: Dynamic copyright information
   - `*|MC_PREVIEW_TEXT|*`: Zero-height preheader block

---

## 3. Client-Specific Solutions

### A. Gmail App (iOS & Android)
Gmail does not support `@media (prefers-color-scheme: dark)` in its mobile apps and aggressively recalculates high-contrast colors.
- **The Off-Hex Rule**: Never use pure `#FFFFFF` or pure `#000000`. Use `#FFFFFE` for backgrounds/text and `#121212` / `#0E0E0E` for dark elements. This reduces Gmail's automatic inversion trigger.
- **Transparent PNGs with Halos**: Since Gmail will not swap images via CSS, all logos, badges, and text-based graphics must be transparent 24-bit PNGs. Dark text elements within graphics must have a soft translucent outer halo (`rgba(255, 255, 255, 0.3)`) to remain readable if Gmail turns the container dark gray.

### B. Outlook Desktop (MSO Word Engine)
- Outlook 2016, 2019, and Microsoft 365 on Windows completely ignore CSS gradients, border-radius, and standard flex/grid CSS.
- Use Vector Markup Language (`v:roundrect`, `v:fill`, `w:anchorlock`) for all Call-to-Action (CTA) buttons.
- Wrap alternate dark mode images in conditional comments so they never appear as broken or duplicate images in Outlook desktop:
  ```html
  <!--[if !mso]><! -->
  <div class="dark-img" style="display: none; max-height: 0px; overflow: hidden; mso-hide: all;">
    <img src="..." style="display: none;" />
  </div>
  <!--<![endif]-->
  ```

### C. Outlook Mobile & Outlook.com
- Outlook mobile and web use the `[data-ogsc]` (color) and `[data-ogsb]` (background) attributes.
- Duplicate every rule from your `@media (prefers-color-scheme: dark)` stylesheet under corresponding `[data-ogsc]` and `[data-ogsb]` blocks.

---

## 4. Master Bulletproof Email Template (Mailchimp Ready)

Use this complete template for client deliveries:

```html
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>*|MC:SUBJECT|*</title>

  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->

  <style type="text/css">
    :root {
      color-scheme: light dark;
      supported-color-schemes: light dark;
    }

    /* iOS & Apple Mail Dark Mode Targeting */
    @media (prefers-color-scheme: dark) {
      .bg-body {
        background-color: #121212 !important;
        background-image: linear-gradient(#121212, #121212) !important;
      }
      .bg-card {
        background-color: #1E1E1E !important;
        background-image: linear-gradient(#1E1E1E, #1E1E1E) !important;
      }
      .bg-footer {
        background-color: #161616 !important;
        background-image: linear-gradient(#161616, #161616) !important;
      }
      .text-heading {
        color: #FFFFFE !important;
      }
      .text-body {
        color: #D6D6D6 !important;
      }
      .text-muted {
        color: #8C8C8C !important;
      }
      .btn-bg {
        background-color: #3B82F6 !important;
        background-image: linear-gradient(#3B82F6, #3B82F6) !important;
      }
      .light-image {
        display: none !important;
      }
      .dark-image-wrapper,
      .dark-image {
        display: block !important;
        max-height: none !important;
        overflow: visible !important;
      }
    }

    /* Outlook Web & Mobile (data-ogsc / data-ogsb) Targeting */
    [data-ogsc] .bg-body {
      background-color: #121212 !important;
      background-image: linear-gradient(#121212, #121212) !important;
    }
    [data-ogsc] .bg-card {
      background-color: #1E1E1E !important;
      background-image: linear-gradient(#1E1E1E, #1E1E1E) !important;
    }
    [data-ogsc] .bg-footer {
      background-color: #161616 !important;
      background-image: linear-gradient(#161616, #161616) !important;
    }
    [data-ogsc] .text-heading {
      color: #FFFFFE !important;
    }
    [data-ogsc] .text-body {
      color: #D6D6D6 !important;
    }
    [data-ogsc] .text-muted {
      color: #8C8C8C !important;
    }
    [data-ogsc] .btn-bg {
      background-color: #3B82F6 !important;
      background-image: linear-gradient(#3B82F6, #3B82F6) !important;
    }
    [data-ogsc] .light-image {
      display: none !important;
    }
    [data-ogsc] .dark-image-wrapper,
    [data-ogsc] .dark-image {
      display: block !important;
      max-height: none !important;
      overflow: visible !important;
    }

    /* Base Reset */
    body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse; }
    img { -ms-interpolation-mode: bicubic; border: 0; outline: none; text-decoration: none; display: block; }
  </style>
</head>
<body class="bg-body" style="margin: 0; padding: 0; width: 100% !important; background-color: #F4F4F4; background-image: linear-gradient(#F4F4F4, #F4F4F4);">

  <!-- Mailchimp Invisible Preheader Anti-Seam Wrapper -->
  <span style="display: none; font-size: 0px; line-height: 0px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; visibility: hidden; mso-hide: all;">
    *|MC_PREVIEW_TEXT|*
  </span>

  <!-- Outer Canvas Table -->
  <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" class="bg-body" style="background-color: #F4F4F4; background-image: linear-gradient(#F4F4F4, #F4F4F4);">
    <tr>
      <td align="center" style="padding: 24px 12px;">

        <!-- Main Email Container (600px Max) -->
        <!--[if (gte mso 9)|(IE)]>
        <table role="presentation" align="center" border="0" cellspacing="0" cellpadding="0" width="600">
        <tr>
        <td align="center" valign="top" width="600">
        <![endif]-->
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" class="bg-card" style="max-width: 600px; background-color: #FFFFFE; background-image: linear-gradient(#FFFFFE, #FFFFFE); border-radius: 8px; overflow: hidden;">

          <!-- HERO BANNER ROW (Zero-Seam Image Integration) -->
          <tr>
            <td align="center" bgcolor="#FFFFFE" class="bg-card" style="padding: 0; margin: 0; background-color: #FFFFFE; background-image: linear-gradient(#FFFFFE, #FFFFFE);">
              
              <!-- Light Mode Hero Image -->
              <img class="light-image" 
                   src="https://via.placeholder.com/600x260/FFFFFE/111111?text=Campaign+Hero" 
                   width="600" 
                   alt="Campaign Banner" 
                   style="width: 100%; max-width: 600px; height: auto; display: block; border: 0;" />

              <!-- Alternate Dark Mode Hero Image (Hidden in MSO) -->
              <!--[if !mso]><! -->
              <div class="dark-image-wrapper" style="display: none; max-height: 0px; overflow: hidden; mso-hide: all;">
                <img class="dark-image" 
                     src="https://via.placeholder.com/600x260/1E1E1E/FFFFFE?text=Campaign+Hero+Dark" 
                     width="600" 
                     alt="Campaign Banner" 
                     style="display: none; width: 100%; max-width: 600px; height: auto; border: 0;" />
              </div>
              <!--<![endif]-->

            </td>
          </tr>

          <!-- MAIN CONTENT BODY -->
          <tr>
            <td style="padding: 36px 28px 24px 28px; text-align: left;">
              <div mc:edit="main_copy">
                <h1 class="text-heading" style="margin: 0 0 16px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 24px; line-height: 32px; color: #111111; font-weight: 700;">
                  Bulletproof Email Architecture
                </h1>
                <p class="text-body" style="margin: 0 0 24px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; color: #444444;">
                  This design maintains background color harmony across iOS Mail, Gmail, and Outlook. The CTA below uses hybrid VML and CSS to preserve styling in all environments.
                </p>
              </div>

              <!-- BULLETPROOF BUTTON (VML for Outlook Desktop + CSS for Modern Clients) -->
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="left" style="padding-top: 8px; padding-bottom: 8px;">
                    <div>
                      <!--[if mso]>
                      <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://example.com" style="height:48px;v-text-anchor:middle;width:200px;" arcsize="10%" strokecolor="#1D4ED8" fillcolor="#2563EB">
                        <w:anchorlock/>
                        <center style="color:#ffffff;font-family:sans-serif;font-size:16px;font-weight:bold;">
                          Take Action Now
                        </center>
                      </v:roundrect>
                      <![endif]-->
                      <!--[if !mso]><! -->
                      <a href="https://example.com" class="btn-bg" style="display: inline-block; background-color: #2563EB; background-image: linear-gradient(#2563EB, #2563EB); color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 600; line-height: 48px; text-align: center; text-decoration: none; width: 200px; -webkit-text-size-adjust: none; border-radius: 6px;">
                        <span mc:edit="cta_label" style="color: #ffffff;">Take Action Now</span>
                      </a>
                      <!--<![endif]-->
                    </div>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- COMPLIANT MAILCHIMP FOOTER -->
          <tr>
            <td class="bg-footer" bgcolor="#F8F8F8" style="padding: 24px 28px; background-color: #F8F8F8; background-image: linear-gradient(#F8F8F8, #F8F8F8); border-top: 1px solid #EAEAEA;">
              <div mc:edit="footer_copy">
                <p class="text-muted" style="margin: 0 0 12px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 12px; line-height: 18px; color: #777777;">
                  You received this email because you signed up for updates from *|LIST:COMPANY|*.
                </p>
                <p class="text-muted" style="margin: 0 0 12px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 12px; line-height: 18px; color: #777777;">
                  *|LIST:ADDRESSLINE|*
                </p>
                <p class="text-muted" style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 12px; line-height: 18px; color: #777777;">
                  <a href="*|UPDATE_PROFILE|*" style="color: #2563EB; text-decoration: underline;">Update Preferences</a>
                  &nbsp;&bull;&nbsp;
                  <a href="*|UNSUB|*" style="color: #2563EB; text-decoration: underline;">Unsubscribe</a>
                  &nbsp;&bull;&nbsp;
                  <a href="*|ARCHIVE|*" style="color: #2563EB; text-decoration: underline;">View in Browser</a>
                </p>
              </div>
            </td>
          </tr>

        </table>
        <!--[if (gte mso 9)|(IE)]>
        </td>
        </tr>
        </table>
        <![endif]-->

      </td>
    </tr>
  </table>

</body>
</html>
```

---

## 5. Automated Bulk Verification Rules

Before delivering HTML to Mailchimp or finalizing builds in Antigravity, verify the following checklist:

1. **Dual Tagging**: Both `<meta name="color-scheme" content="light dark">` and `<meta name="supported-color-schemes" content="light dark">` are present in `<head>`.
2. **Duplicate Query Coverage**: Every dark selector in `@media (prefers-color-scheme: dark)` has an identical declaration inside `[data-ogsc]`.
3. **Linear Gradient Lock**: Every `<td>`, `<table>`, and `<a>` container with a color declaration uses `background-image: linear-gradient(#HEX, #HEX)` alongside `background-color`.
4. **Transparent Asset Standard**: Badges, logos, and overlaid graphics use 24-bit transparent PNGs with a subtle light stroke/halo for dark mode contrast.
5. **VML Dual-Path Buttons**: CTAs include a `<v:roundrect>` block for Outlook desktop alongside an `<!--[if !mso]><! -->` anchor block for mobile and modern web clients.
6. **Mailchimp Node Isolation**: All `mc:edit` tags are placed on inner text tags (`<div>`, `<p>`, `<span>`) rather than table cells (`<td>`) that have gradient styles.
7. **CAN-SPAM / Legal Tags**: All required merge tags (`*|UNSUB|*`, `*|LIST:ADDRESSLINE|*`, `*|LIST:COMPANY|*`) are present in the footer.