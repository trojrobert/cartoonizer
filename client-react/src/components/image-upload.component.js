import React, { Component } from "react";
import UploadService from "../services/file-upload.service";

export default class UploadImages extends Component {
  constructor(props) {
    super(props);
    this.selectFile = this.selectFile.bind(this);
    this.upload = this.upload.bind(this);

    this.state = {
      currentFile: undefined,
      previewImage: undefined,
      predictImage: undefined, 
      progress: 0,
      message: "",
      imageInfos: [],
    };
  }

  selectFile(event) {
    this.setState({
      currentFile: event.target.files[0],
      previewImage: URL.createObjectURL(event.target.files[0]),
      progress: 0,
      message: "File Selected. Please click Colourize"
    });
  }

  upload() {
    this.setState({
      progress: 0,
    });

    UploadService.upload(this.state.currentFile, (event) => {
      this.setState({
        progress: Math.round((100 * event.loaded) / event.total),
      });
    })
    .then((response) => {
      console.log(response)
      this.setState({
        predictImage: `data:image/jpeg;base64,${response}`,
      });
      })
  }

  render() {
    const {
      currentFile,
      previewImage,
      predictImage,
      progress,
      message,
      imageInfos,
    } = this.state;

    return (
      <div>
        <div className="row">
          <div className="col-8">
            <label className="btn btn-default p-0">
              <input type="file" accept="image/*" onChange={this.selectFile} />
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

        {currentFile && (
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
        )}

        {previewImage && (
          <div>
              <img className="col-md-4 img-responsive" src={previewImage} width="300" height="300" alt="" />

              <img className="col-md-4 img-responsive" src={predictImage} width="300" height="300" alt="" />
          </div>
        )}

        {/* {message && (
          <div className="alert alert-secondary mt-3" role="alert">
            {message}
          </div> 
        )} */}

        {/* {predictImage && (
          <div>
            <img className="preview" src={predictImage} alt="" />
          </div> 
        )} */}

        {/* <div className="card mt-3">
          <div className="card-header">List of Images</div>
          <ul className="list-group list-group-flush">
            {imageInfos &&
              imageInfos.map((img, index) => (
                <li className="list-group-item" key={index}>
                  <a href={img.url}>{img.name}</a>
                </li>
              ))}
          </ul>
        </div> */}
      </div>
    );
  }
}