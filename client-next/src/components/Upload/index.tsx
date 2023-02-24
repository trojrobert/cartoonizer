import Image from "next/image";
import React, { useCallback, useState } from "react";
import UploadService from "@/services/upload.service";
import "bootstrap/dist/css/bootstrap.min.css";

const Upload = () => {
  const [previewImage, setPreviewImage] = useState<any>(null);
  const [decolorizedImage, setDecolorizedImage] = useState<string>();

  const handleImageUpload = useCallback((event: any) => {
    const file = event.target.files[0];
    // const progress = Math.round((100 * event.loaded) / event.total);
    setPreviewImage(file);
  }, []);

  const handleClick = useCallback(async (previewImage) => {
    console.log("console image", previewImage);

    const response = await UploadService.upload(previewImage);

    setDecolorizedImage(response);
  }, []);

  return (
    <div>
      <div className="row">
        <div className="col-8">
          <label className="btn btn-default p-0">
            <input type="file" accept="image/*" onChange={handleImageUpload} />
          </label>
        </div>

        <div className="col-4">
          <button
            className="btn btn-success btn-sm"
            disabled={!previewImage}
            onClick={() => handleClick(previewImage)}
          >
            Decolourize
          </button>
        </div>
      </div>

      {/* {currentFile && (
        <div className="progress my-3">
          <div
            className="progress-bar progress-bar-info progress-bar-striped"
            role="progressbar"
            aria-valuenow={progress}
            aria-valuemin="0"
            aria-valuemax="100"
            style={{ width: progress + "%" }}
          >
            {progress}%
          </div>
        </div>
      )} */}

      {previewImage && (
        <div style={{ width: "300px", height: "300px" }}>
          <Image
            alt=""
            loading="lazy"
            src={URL.createObjectURL(previewImage)}
            width="300"
            height="300"
            layout="cover"
          />
        </div>
      )}
      {decolorizedImage && (
        <div style={{ width: "300px", height: "300px" }}>
          <Image
            alt=""
            loading="lazy"
            src={decolorizedImage}
            width="300"
            height="300"
          />
        </div>
      )}
    </div>
  );
};

export default Upload;
