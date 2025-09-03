import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "@/ui/globals.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import BootstrapClient from '@/common/bootstrapclient';


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "MetaBuild",
  description: "PC builder app by Ahmed",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
        <BootstrapClient />
      </body>
    </html>
  );
}
