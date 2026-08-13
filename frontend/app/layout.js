import "./globals.css";

export const metadata = {
  title: "NyayBase - Legal Case Analysis for India",
  description:
    "Predict court case outcomes, discover winning arguments, and get legal strategy analysis based on 1.2M+ Indian court judgments.",
  keywords: "legal analysis, court case predictor, Indian law, case outcome, legal strategy",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
