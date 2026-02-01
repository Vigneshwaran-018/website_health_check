# Frontend - Health Check Dashboard

Modern React dashboard for visualizing website security audit results. Built with Vite, React, Tailwind CSS, and Recharts.

## Features

- **Interactive Dashboard**: Real-time display of security scan results
- **Risk Score Visualization**: Gauge chart showing overall security score
- **Security Headers Overview**: Visual representation of missing/present headers
- **Open Ports Detection**: Interactive list of discovered open ports
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Deployment Ready**: Pre-configured for Vercel deployment

## Technology Stack

- **React 18**: UI library
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: React charting library
- **Axios**: HTTP client for API communication

## Installation

### Prerequisites
- Node.js 16+ and npm

### Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file for development:
```bash
VITE_API_URL=http://localhost:8000
```

## Running Locally

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

```bash
npm run build
```

This generates optimized production build in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx              # Navigation header
│   │   ├── URLInput.jsx            # URL input form
│   │   ├── RiskScoreCard.jsx       # Risk score gauge
│   │   ├── SSLStatusCard.jsx       # SSL/TLS info
│   │   ├── SecurityHeadersCard.jsx # Headers status
│   │   ├── OpenPortsCard.jsx       # Open ports list
│   │   ├── DeductionsTable.jsx     # Score breakdown
│   │   ├── LoadingSpinner.jsx      # Loading state
│   │   ├── ErrorDisplay.jsx        # Error messages
│   │   └── Footer.jsx              # Footer
│   ├── services/
│   │   └── api.js                  # API client service
│   ├── config.js                   # Configuration utilities
│   ├── App.jsx                     # Main app component
│   ├── main.jsx                    # Entry point
│   └── index.css                   # Global styles
├── index.html                      # HTML template
├── vite.config.js                  # Vite configuration
├── tailwind.config.js              # Tailwind configuration
├── postcss.config.js               # PostCSS configuration
└── package.json                    # Dependencies and scripts
```

## Configuration

### Environment Variables

Create a `.env.local` file in the frontend root:

```env
# API endpoint (development)
VITE_API_URL=http://localhost:8000

# Production API endpoint
# VITE_API_URL=https://api.yourdomain.com
```

### API Service

The API client is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

Switch API endpoints by updating the environment variable.

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub

2. Import project in Vercel dashboard

3. Set environment variables:
   - `VITE_API_URL`: Your backend API URL

4. Deploy

```bash
# Or use Vercel CLI
npm install -g vercel
vercel
```

### Netlify

1. Connect GitHub repository to Netlify

2. Build command: `npm run build`

3. Publish directory: `dist`

4. Set environment variables in Netlify dashboard

5. Deploy

### Docker

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and run:

```bash
docker build --build-arg VITE_API_URL=http://your-api.com -t health-check-dashboard .
docker run -p 80:80 health-check-dashboard
```

## Components

### URLInput
Handles user input for website URL with validation and error messages.

### RiskScoreCard
Displays overall security risk score using a donut/gauge chart powered by Recharts.

### SSLStatusCard
Shows SSL/TLS certificate information:
- Certificate validity status
- Issued to/by information
- Expiration timeline
- Protocol version and cipher suite

### SecurityHeadersCard
Lists present and missing security headers:
- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options

### OpenPortsCard
Displays detected open ports with service identification and risk levels.

### DeductionsTable
Breaks down the risk score calculation with category, issue, and deduction amount.

## Development

### Hot Module Replacement (HMR)
Vite provides instant HMR for React components during development.

### Styling
Tailwind CSS is configured with custom theme colors:
- `primary-*`: Primary blue color scheme
- `success`, `warning`, `error`: Status colors

### Adding New Components

1. Create new `.jsx` file in `src/components/`
2. Import and use in `App.jsx` or other components
3. Styles use Tailwind classes for consistency

## Performance Optimization

- Code splitting via Vite
- Image optimization with lazy loading ready
- CSS minification in production build
- No unnecessary re-renders with React.memo (when needed)

## Troubleshooting

**Issue: Cannot connect to backend**
- Verify backend is running: `http://localhost:8000`
- Check `VITE_API_URL` environment variable
- Ensure CORS is configured on backend

**Issue: Build fails**
- Clear `node_modules/` and reinstall: `npm install`
- Check Node.js version: `node --version` (should be 16+)

**Issue: Styling not applied**
- Rebuild Tailwind: Delete `node_modules/.vite` and restart dev server

## License

This project is provided as-is for educational and authorized testing purposes.
