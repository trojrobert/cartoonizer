import Image from 'next/image';
import React, { useCallback } from 'react';
import UploadService from '@/services/upload.service';

const Upload = () => {
const [previewImage, setPreviewImage] = useState();

const handleImageUpload = useCallback(async (event: any) => {
  const file = event.target.files[0];
  // const progress = Math.round((100 * event.loaded) / event.total);
  const response = await UploadService.upload(file);

  setPreviewImage(`data:image/jpeg;base64,${response}`);
},[]);

  return
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
            disabled={!currentFile}
            onClick={this.upload}
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
        <Image loading="lazy" src={previewImage} width="300" height="300" objectFit="fill" layout="responsive" />
      )}
    </div>
  );
}

export default Upload;
