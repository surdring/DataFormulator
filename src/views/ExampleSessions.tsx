// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

import React from 'react';
import {
    Typography,
    Box,
    Card,
    CardContent,
    Chip,
    alpha,
    useTheme,
} from '@mui/material';
import { t } from '../i18n';

// Example session data for pre-built sessions
export interface ExampleSession {
    id: string;
    title: string;
    description: string;
    previewImage: string;
    dataFile: string;
}

export const exampleSessions: ExampleSession[] = [
    {
        id: 'gas-prices',
        title: t('examples.gasPrices.title'),
        description: t('examples.gasPrices.desc'),
        previewImage: '/gas_prices-thumbnail.webp',
        dataFile: '/df_gas_prices.json',
    },
    {
        id: 'global-energy',
        title: t('examples.globalEnergy.title'),
        description: t('examples.globalEnergy.desc'),
        previewImage: '/global_energy-thumbnail.webp',
        dataFile: '/df_global_energy.json',
    },
    {
        id: 'movies',
        title: t('examples.movies.title'),
        description: t('examples.movies.desc'),
        previewImage: '/movies-thumbnail.webp',
        dataFile: '/df_movies.json',
    },
    {
        id: 'unemployment',
        title: t('examples.unemployment.title'),
        description: t('examples.unemployment.desc'),
        previewImage: '/unemployment-thumbnail.webp',
        dataFile: '/df_unemployment.json',
    }
];

// Session card component for displaying example sessions
export const ExampleSessionCard: React.FC<{
    session: ExampleSession;
    theme: any;
    onClick: () => void;
    disabled?: boolean;
}> = ({ session, theme, onClick, disabled }) => {
    return (
        <Card
            sx={{
                width: 240,
                borderRadius: 3,
                border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                transition: 'all 0.3s ease-in-out',
                cursor: disabled ? 'default' : 'pointer',
                opacity: disabled ? 0.6 : 1,
                position: 'relative',
                overflow: 'hidden',
                '&:hover': disabled ? {} : {
                    boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
                    transform: 'translateY(-2px)',
                    borderColor: alpha(theme.palette.primary.main, 0.4),
                },
            }}
            onClick={disabled ? undefined : onClick}
        >
            <Box
                sx={{
                    height: 100,
                    background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.custom.main, 0.1)} 100%)`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    position: 'relative',
                    overflow: 'hidden'
                }}
            >
                <Box
                    component="img"
                    src={session.previewImage}
                    alt={session.title}
                    sx={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover',
                        opacity: 0.8
                    }}
                />
            </Box>

            {/* Content */}
            <CardContent sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', py: 1,
                '&:last-child': { pb: 1 }
             }}>
                {/* Header */}
                <Box>
                    <Typography
                        variant="subtitle2"
                        sx={{
                            fontSize: '12px',
                            color: theme.palette.text.secondary,
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical',
                            overflow: 'hidden'
                        }}
                    >
                        <span style={{textDecoration: 'underline'}}>{session.title}:</span> {session.description}
                    </Typography>
                </Box>
            </CardContent>
        </Card>
    );
};
