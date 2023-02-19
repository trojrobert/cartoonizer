class UploadService {
  static async upload(file: string | undefined) {
    try {
      const response = await fetch("http://0.0.0.0:8080/decolorize", {
        method: "POST",
        body: JSON.stringify({file})
      });

      const data = await response.json();

      return Promise.resolve(data);
    }
    catch (err) {
      throw new Error('Upload failed');

    }
  }
}

export default UploadService;
