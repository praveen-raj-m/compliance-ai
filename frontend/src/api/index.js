// API base URL - change according to your deployment
const API_BASE_URL = "http://localhost:5001/api";

/**
 * Fetches all available compliance standards
 * @returns {Promise<string[]>} Array of standard names
 */
export async function fetchStandards() {
  try {
    const response = await fetch(`${API_BASE_URL}/standards`);
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    const data = await response.json();
    return data.standards || [];
  } catch (error) {
    console.error("Error fetching standards:", error);
    return [];
  }
}

/**
 * Submits a query about compliance standards
 * @param {string} query - The user's question
 * @param {string} [standard] - Optional: The specific compliance standard to query (if omitted, searches all standards)
 * @returns {Promise<Object>} The answer with metadata
 */
export async function submitQuery(query, standard = null) {
  try {
    const payload = { query };
    if (standard) {
      payload.standard = standard;
    }

    console.log(query, API_BASE_URL);

    const response = await fetch(`${API_BASE_URL}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();

    // Format the response for the UI
    return {
      answer: data.answer,
      sources: data.sources || [],
      success: data.success !== false,
      // Format the answer with the sources for display
      formattedAnswer: formatAnswer(data.answer, data.sources),
    };
  } catch (error) {
    console.error("Error submitting query:", error);
    throw error;
  }
}

/**
 * Format the answer with source information for display
 */
function formatAnswer(answer, sources) {
  if (!sources || sources.length === 0) {
    return answer;
  }

  // Format the sources into a string
  const sourcesText = sources
    .map((source, index) => {
      return `Source ${index + 1}: ${source.source} - Article ${
        source.article
      } (${source.title || "N/A"})`;
    })
    .join("\n");

  return `${answer}\n\nSources:\n${sourcesText}`;
}

/**
 * Uploads a company policy and compares it against a standard
 * @param {File} file - The policy file to upload
 * @param {string} standard - The compliance standard to compare against
 * @returns {Promise<Object>} The compliance analysis results
 */
export async function comparePolicy(file, standard) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("standard", standard);

    const response = await fetch(`${API_BASE_URL}/compare`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error comparing policy:", error);
    throw error;
  }
}

/**
 * Uploads a new compliance standard document
 * @param {File} file - The standard document to upload
 * @param {string} standardName - The name of the standard
 * @returns {Promise<Object>} Upload status
 */
export async function uploadStandard(file, standardName) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", standardName);

    const response = await fetch(`${API_BASE_URL}/upload-standard`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error uploading standard:", error);
    throw error;
  }
}
