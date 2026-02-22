---
name: email-resend
description: Email sending via Resend API for contact forms and booking requests with locale-aware templates. Use when implementing email notifications, contact form submissions, or transactional emails.
---

# Email with Resend

## Environment Setup

```bash
# .env.local
RESEND_API_KEY=re_...
CONTACT_TO_EMAIL=hello@studioname.com
```

## Resend Client

```tsx
// lib/resend.ts
import { Resend } from 'resend';

export const resend = process.env.RESEND_API_KEY
  ? new Resend(process.env.RESEND_API_KEY)
  : null;

export function hasResend(): boolean {
  return resend !== null;
}
```

## Contact Form Email

```tsx
// lib/emails/contact.ts
import { resend } from '@/lib/resend';
import type { Locale } from '@/i18n.config';

interface ContactEmailParams {
  name: string;
  email: string;
  phone?: string;
  message: string;
  locale: Locale;
}

export async function sendContactEmail({
  name,
  email,
  phone,
  message,
  locale,
}: ContactEmailParams) {
  if (!resend) {
    console.log('Resend not configured, skipping email');
    return { success: false, error: 'Email not configured' };
  }

  const toEmail = process.env.CONTACT_TO_EMAIL!;

  try {
    await resend.emails.send({
      from: 'Studio Contact <noreply@studioname.com>',
      to: toEmail,
      replyTo: email,
      subject: `New Contact Form Submission from ${name}`,
      html: `
        <h2>New Contact Form Submission</h2>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        ${phone ? `<p><strong>Phone:</strong> ${phone}</p>` : ''}
        <p><strong>Message:</strong></p>
        <p>${message.replace(/\n/g, '<br>')}</p>
        <hr>
        <p><small>Submitted from: ${locale} locale</small></p>
      `,
    });

    return { success: true };
  } catch (error) {
    console.error('Failed to send email:', error);
    return { success: false, error: 'Failed to send email' };
  }
}
```

## Booking Request Email

```tsx
// lib/emails/booking.ts
import { resend } from '@/lib/resend';
import type { Locale } from '@/i18n.config';

interface BookingEmailParams {
  name: string;
  email: string;
  phone?: string;
  goals: string;
  experienceLevel: string;
  injuries?: string;
  preferredTimes: string;
  sessionType: 'in-person' | 'online';
  locale: Locale;
}

const subjectByLocale: Record<Locale, string> = {
  'pt-PT': 'Novo Pedido de Sessão',
  'en': 'New Booking Request',
  'tr': 'Yeni Rezervasyon Talebi',
  'es': 'Nueva Solicitud de Reserva',
  'fr': 'Nouvelle Demande de Réservation',
  'de': 'Neue Buchungsanfrage',
};

export async function sendBookingEmail(params: BookingEmailParams) {
  if (!resend) {
    console.log('Resend not configured, skipping email');
    return { success: false, error: 'Email not configured' };
  }

  const toEmail = process.env.CONTACT_TO_EMAIL!;

  try {
    // Email to studio
    await resend.emails.send({
      from: 'Studio Booking <noreply@studioname.com>',
      to: toEmail,
      replyTo: params.email,
      subject: `${subjectByLocale[params.locale]}: ${params.name}`,
      html: generateBookingHtml(params),
    });

    // Confirmation email to client
    await resend.emails.send({
      from: 'Studio Name <noreply@studioname.com>',
      to: params.email,
      subject: getConfirmationSubject(params.locale),
      html: generateConfirmationHtml(params),
    });

    return { success: true };
  } catch (error) {
    console.error('Failed to send booking email:', error);
    return { success: false, error: 'Failed to send email' };
  }
}

function generateBookingHtml(params: BookingEmailParams): string {
  return `
    <h2>New Booking Request</h2>
    <table style="border-collapse: collapse; width: 100%;">
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Name</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.name}</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Email</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.email}</td>
      </tr>
      ${params.phone ? `
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Phone</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.phone}</td>
      </tr>
      ` : ''}
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Session Type</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.sessionType}</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Experience</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.experienceLevel}</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Goals</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.goals}</td>
      </tr>
      ${params.injuries ? `
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Injuries/Notes</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.injuries}</td>
      </tr>
      ` : ''}
      <tr>
        <td style="padding: 8px; border: 1px solid #ddd;"><strong>Preferred Times</strong></td>
        <td style="padding: 8px; border: 1px solid #ddd;">${params.preferredTimes}</td>
      </tr>
    </table>
    <p><small>Locale: ${params.locale}</small></p>
  `;
}

function getConfirmationSubject(locale: Locale): string {
  const subjects: Record<Locale, string> = {
    'pt-PT': 'Recebemos o seu pedido de sessão',
    'en': 'We received your booking request',
    'tr': 'Rezervasyon talebinizi aldık',
    'es': 'Recibimos tu solicitud de reserva',
    'fr': 'Nous avons reçu votre demande',
    'de': 'Wir haben Ihre Anfrage erhalten',
  };
  return subjects[locale];
}

function generateConfirmationHtml(params: BookingEmailParams): string {
  // Localized confirmation message
  return `
    <h2>Thank you for your booking request!</h2>
    <p>Hi ${params.name},</p>
    <p>We've received your request and will get back to you within 24 hours.</p>
    <p>Best regards,<br>Studio Name</p>
  `;
}
```

## Server Action with Email

```tsx
// lib/actions/contact.ts
'use server';

import { contactFormSchema } from '@/lib/validations';
import { sendContactEmail } from '@/lib/emails/contact';
import type { Locale } from '@/i18n.config';

export async function submitContactForm(formData: FormData, locale: Locale) {
  const rawData = {
    name: formData.get('name'),
    email: formData.get('email'),
    phone: formData.get('phone'),
    message: formData.get('message'),
  };

  const result = contactFormSchema.safeParse(rawData);

  if (!result.success) {
    return {
      success: false,
      errors: result.error.flatten().fieldErrors,
    };
  }

  const emailResult = await sendContactEmail({
    ...result.data,
    locale,
  });

  if (!emailResult.success) {
    return {
      success: false,
      errors: { _form: ['Failed to send message. Please try again.'] },
    };
  }

  return { success: true };
}
```

## Fallback Without Resend

```tsx
// When RESEND_API_KEY is not set
export function ContactForm() {
  const hasEmail = hasResend();

  if (!hasEmail) {
    return (
      <div className="text-center p-8">
        <p>Contact us directly at:</p>
        <a href="mailto:hello@studioname.com" className="text-primary">
          hello@studioname.com
        </a>
      </div>
    );
  }

  return <ContactFormWithEmail />;
}
```
