import json


class ResponseFormatter:
    """
    Service responsible for formatting Gemini responses
    into a structured dictionary.
    """

    @staticmethod
    def format_response(
        response_text: str,
    ) -> dict:
        """
        Convert a Gemini response into a structured format.

        Expected Gemini response:

        {
            "answer": "...",
            "career": "...",
            "resources": [
                "...",
                "..."
            ]
        }

        If the response is not valid JSON,
        the raw response is returned as the answer.
        """

        try:
            data = json.loads(response_text)

            return {
                "answer": (
                    data.get("answer", "").strip()
                    if isinstance(data.get("answer"), str)
                    else ""
                ),
                "career": (
                    data.get("career")
                    if isinstance(data.get("career"), str)
                    else None
                ),
                "resources": (
                    data.get("resources")
                    if isinstance(data.get("resources"), list)
                    else []
                ),
            }

        except (json.JSONDecodeError, TypeError, AttributeError):
            return {
                "answer": response_text.strip(),
                "career": None,
                "resources": [],
            }