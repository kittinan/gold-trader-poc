# Shared Utilities

Gold Trader Shared Utilities and Configurations

## Purpose
This directory contains shared utilities, configurations, and types that are used by both frontend and backend applications.

## Contents
- **types/**: TypeScript type definitions
- **configs/**: Shared configuration files
- **utils/**: Shared utility functions
- **schemas/**: Shared data schemas and validation

## Development
This helps maintain consistency between frontend and backend applications by providing shared:
- Type definitions
- API schemas
- Configuration values
- Utility functions
- Constants and enums

## Structure
```
shared/
├── types/             # TypeScript type definitions
│   ├── api.ts        # API response types
│   ├── user.ts       # User-related types
│   └── trading.ts    # Trading-related types
├── configs/          # Configuration files
│   ├── api.ts        # API configuration
│   └── constants.ts  # Shared constants
├── utils/            # Utility functions
│   ├── validation.ts # Validation functions
│   └── helpers.ts    # Helper functions
└── schemas/          # Data schemas
    ├── user.schema.ts # User data schemas
    └── trading.schema.ts # Trading data schemas
```