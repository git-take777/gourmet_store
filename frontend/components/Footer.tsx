'use client';

import { FC } from 'react';
import Link from 'next/link';
import { Box, Container, Grid, Typography, IconButton, useTheme, useMediaQuery } from '@mui/material';
import { styled } from '@mui/material/styles';
import GitHubIcon from '@mui/icons-material/GitHub';
import TwitterIcon from '@mui/icons-material/Twitter';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

// スタイル付きコンポーネントの定義
const FooterWrapper = styled('footer')(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  padding: theme.spacing(6, 0),
  marginTop: 'auto',
}));

const FooterLink = styled(Link)(({ theme }) => ({
  color: theme.palette.primary.contrastText,
  textDecoration: 'none',
  '&:hover': {
    textDecoration: 'underline',
  },
}));

const Footer: FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const currentYear = new Date().getFullYear();

  return (
    <FooterWrapper>
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          {/* Company Information */}
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              GrubTrack Official
            </Typography>
            <Typography variant="body2">
              Elevating your Minecraft experience with advanced visual effects management.
            </Typography>
          </Grid>

          {/* Quick Links */}
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Quick Links
            </Typography>
            <Box display="flex" flexDirection="column" gap={1}>
              <FooterLink href="/effects">Effects Library</FooterLink>
              <FooterLink href="/dashboard">Dashboard</FooterLink>
              <FooterLink href="/documentation">Documentation</FooterLink>
            </Box>
          </Grid>

          {/* Contact Information */}
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Connect With Us
            </Typography>
            <Box display="flex" gap={2}>
              <IconButton
                aria-label="GitHub"
                color="inherit"
                component="a"
                href="https://github.com/grubtrack"
                target="_blank"
                rel="noopener noreferrer"
              >
                <GitHubIcon />
              </IconButton>
              <IconButton
                aria-label="Twitter"
                color="inherit"
                component="a"
                href="https://twitter.com/grubtrack"
                target="_blank"
                rel="noopener noreferrer"
              >
                <TwitterIcon />
              </IconButton>
              <IconButton
                aria-label="LinkedIn"
                color="inherit"
                component="a"
                href="https://linkedin.com/company/grubtrack"
                target="_blank"
                rel="noopener noreferrer"
              >
                <LinkedInIcon />
              </IconButton>
            </Box>
          </Grid>
        </Grid>

        {/* Copyright Section */}
        <Box
          mt={4}
          pt={3}
          borderTop={1}
          borderColor="rgba(255, 255, 255, 0.1)"
          textAlign="center"
        >
          <Typography variant="body2">
            © {currentYear} GrubTrack Official. All rights reserved.
          </Typography>
          {!isMobile && (
            <Typography variant="caption" display="block" mt={1}>
              Made with ❤️ for the Minecraft community
            </Typography>
          )}
        </Box>
      </Container>
    </FooterWrapper>
  );
};

export default Footer;