const EMPTY_PAN_DATA = {
  pan: null,
  name: null,
  gender: null,
  dob: null,
};

function setJsonHeaders(res) {
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
}

function parseLlmJson(content) {
  if (!content || typeof content !== "string") {
    return { ...EMPTY_PAN_DATA };
  }

  try {
    return JSON.parse(content.trim());
  } catch (_error) {
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      return { ...EMPTY_PAN_DATA };
    }

    try {
      return JSON.parse(jsonMatch[0]);
    } catch (_nestedError) {
      return { ...EMPTY_PAN_DATA };
    }
  }
}

function normalizePanData(data) {
  const normalized = {
    pan: data && data.pan ? String(data.pan).toUpperCase().trim() : null,
    name: data && data.name ? String(data.name).trim() : null,
    gender: data && data.gender ? String(data.gender).trim() : null,
    dob: data && data.dob ? String(data.dob).trim() : null,
  };

  if (normalized.pan && !/^[A-Z]{5}[0-9]{4}[A-Z]$/.test(normalized.pan)) {
    normalized.pan = null;
  }

  return normalized;
}

function stripDataUrlPrefix(image) {
  return String(image || "").replace(/^data:image\/[a-zA-Z0-9.+-]+;base64,/, "");
}

module.exports = async function handler(req, res) {
  setJsonHeaders(res);

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ success: false, error: "Method not allowed", data: {} });
  }

  const base64Image = stripDataUrlPrefix(req.body && req.body.image);
  if (!base64Image) {
    return res.status(400).json({ success: false, error: "No image provided", data: {} });
  }

  const gridApiKey = process.env.GRID_AUTH_TOKEN;
  if (!gridApiKey) {
    return res.status(500).json({ success: false, error: "Grid API not configured", data: {} });
  }

  const gridBaseUrl = (process.env.LITELLM_BASE_URL || "https://grid.ai.juspay.net").replace(/\/+$/, "");
  const gridModel = process.env.GRID_MODEL || "kimi-latest";

  const ocrPrompt = `You are an OCR assistant specialized in extracting information from Indian PAN cards.

Your task is to analyze the provided image of a PAN card and extract the following fields:
- PAN Number (key: "pan"): 10-character alphanumeric in format ABCDE1234F
- Full Name (key: "name"): Name as printed on the card
- Gender (key: "gender"): Extract if visible, typically "Male" or "Female"
- Date of Birth (key: "dob"): Extract in DD/MM/YYYY format if present

Return ONLY a valid JSON object in this exact format:
{
  "pan": "ABCDE1234F",
  "name": "John Doe",
  "gender": "Male",
  "dob": "01/01/1990"
}

If a field is not visible or unclear, use null as the value.
Example: {"pan": "ABCDE1234F", "name": null, "gender": null, "dob": null}

Do not include any markdown formatting, explanations, or additional text.`;

  const payload = {
    model: gridModel,
    messages: [
      {
        role: "system",
        content: "You are an OCR assistant specialized in extracting information from documents. Output only valid JSON.",
      },
      {
        role: "user",
        content: [
          { type: "text", text: ocrPrompt },
          { type: "image_url", image_url: { url: `data:image/jpeg;base64,${base64Image}` } },
        ],
      },
    ],
    max_tokens: 1024,
    temperature: 0.2,
  };

  try {
    const response = await fetch(`${gridBaseUrl}/v1/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${gridApiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      return res.status(502).json({
        success: false,
        error: `Grid API error: ${response.status}`,
        data: {},
      });
    }

    const responseData = await response.json();
    const llmResponse = responseData && responseData.choices && responseData.choices[0]
      ? responseData.choices[0].message && responseData.choices[0].message.content
      : "";
    const extractedData = normalizePanData(parseLlmJson(llmResponse));

    return res.status(200).json({
      success: true,
      data: extractedData,
      error: null,
    });
  } catch (error) {
    return res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : "PAN extraction failed",
      data: {},
    });
  }
};

module.exports.config = {
  maxDuration: 60,
};
