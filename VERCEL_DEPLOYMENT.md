# Vercel Deployment

This project is now set up as a static Vercel app with small serverless API functions for the OTP mocks and Grid AI PAN extraction.

## Project settings

- Framework preset: Other
- Build command: leave empty
- Output directory: `public`
- Install command: leave empty unless Vercel asks to install project tooling

## Environment variables

Add these in Vercel Project Settings > Environment Variables:

- `GRID_AUTH_TOKEN`: required for PAN extraction
- `LITELLM_BASE_URL`: optional, defaults to `https://grid.ai.juspay.net`
- `GRID_MODEL`: optional, defaults to `kimi-latest`

## Routes

- `/` and `/otp` open the OTP screen.
- Other screens use clean routes such as `/eligibility-check`, `/choose-plan`, and `/all-set`.
- The AI endpoint is `/api/extract-pan`.
- Old `/api/demonstration/...` page and API URLs are still supported through Vercel rewrites.
