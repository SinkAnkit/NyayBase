import "./globals.css";

export const metadata = {
  title: "NyayBase — AI-Powered Legal Intelligence for India",
  description:
    "Predict court case outcomes, discover winning arguments, and get AI-powered legal strategy advice based on analysis of 1.2M+ Indian court judgments.",
  keywords: "legal AI, court case predictor, Indian law, case outcome, legal strategy",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
