function setJsonHeaders(res) {
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
}

module.exports = function handler(req, res) {
  setJsonHeaders(res);

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ valid: false, error: "Method not allowed" });
  }

  const otp = String((req.body && req.body.otp) || "");

  if (!otp) {
    return res.status(400).json({ valid: false, error: "OTP is required" });
  }

  if (!/^\d+$/.test(otp)) {
    return res.status(400).json({ valid: false, error: "OTP must contain only numbers" });
  }

  if (otp.length !== 6) {
    return res.status(400).json({ valid: false, error: "OTP must be 6 digits" });
  }

  return res.status(200).json({ valid: true, message: "OTP verified successfully" });
};
