def analyze_sentiment(text_content: str, language_code: str = "ko") -> dict:
    from google.cloud import language_v2

    client = language_v2.LanguageServiceClient()
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT
    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }
    encoding_type = language_v2.EncodingType.UTF8
    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )
    result = {
        "score": response.document_sentiment.score,
        "magnitude": response.document_sentiment.magnitude,
        "sentences": [
            {
                "text": s.text.content,
                "score": s.sentiment.score,
                "magnitude": s.sentiment.magnitude,
            }
            for s in response.sentences
        ],
        "language": response.language_code,
    }
    return result
