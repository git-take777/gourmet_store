import type { Metadata } from 'next'
import { Suspense } from 'react'
import dynamic from 'next/dynamic'
import { Container, Grid, Typography, Box } from '@mui/material'

// Dynamic imports for client components
const EffectList = dynamic(() => import('@/components/Effects/EffectList'), {
  ssr: true,
  loading: () => <Loading />
})

const TriggerList = dynamic(() => import('@/components/TriggerList'), {
  ssr: true,
  loading: () => <Loading />
})

import Loading from '@/components/Common/Loading'
import { fetchEffects } from '@/lib/api/effects'
import { fetchTriggers } from '@/lib/api/triggers'

// Metadata for SEO
export const metadata: Metadata = {
  title: 'GrubTrack - Minecraft Effect Management System',
  description: 'Manage and control your Minecraft effects and triggers efficiently',
  keywords: 'minecraft, effects, triggers, gaming, management',
  openGraph: {
    title: 'GrubTrack - Minecraft Effect Management',
    description: 'Professional Minecraft effect management system',
    type: 'website',
  },
}

// Server Component
async function MainPage() {
  // Fetch initial data
  const effects = await fetchEffects()
  const triggers = await fetchTriggers()

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography 
          variant="h1" 
          component="h1" 
          sx={{
            fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
            mb: 4,
            textAlign: 'center'
          }}
        >
          Welcome to GrubTrack
        </Typography>

        <Grid container spacing={4}>
          {/* Effects Section */}
          <Grid item xs={12} md={6}>
            <Typography 
              variant="h2" 
              component="h2" 
              sx={{ 
                fontSize: { xs: '1.5rem', sm: '1.75rem', md: '2rem' },
                mb: 2 
              }}
            >
              Active Effects
            </Typography>
            <Suspense fallback={<Loading />}>
              <EffectList initialEffects={effects} />
            </Suspense>
          </Grid>

          {/* Triggers Section */}
          <Grid item xs={12} md={6}>
            <Typography 
              variant="h2" 
              component="h2" 
              sx={{ 
                fontSize: { xs: '1.5rem', sm: '1.75rem', md: '2rem' },
                mb: 2 
              }}
            >
              Available Triggers
            </Typography>
            <Suspense fallback={<Loading />}>
              <TriggerList initialTriggers={triggers} />
            </Suspense>
          </Grid>
        </Grid>
      </Box>

      {/* Dashboard Preview Section */}
      <Box sx={{ mt: 6, mb: 4 }}>
        <Typography 
          variant="h3" 
          component="h3"
          sx={{ 
            fontSize: { xs: '1.25rem', sm: '1.5rem', md: '1.75rem' },
            mb: 2 
          }}
        >
          System Overview
        </Typography>
        <Grid container spacing={2}>
          {/* Add dashboard widgets here */}
        </Grid>
      </Box>
    </Container>
  )
}

export default MainPage