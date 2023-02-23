class UploadService {
  static async upload(file: Blob | undefined) {
    const formData = new FormData();

    try {
      const response = await fetch("http://0.0.0.0:8080/decolorize", {
        method: "POST",
        body: formData.append("file", file, file.name)
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
