class FileService:
    @staticmethod
    def save_response_to_file(response, filename):
        """
        Save the response content to a file.

        :param response: The response object from the request.
        :param filename: The name of the file to save the response to.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Resposta do servidor salva em {filename}")
