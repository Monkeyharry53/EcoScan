const videoFeed = document.getElementById('video-feed');
const captureButton = document.getElementById('capture-button');
const capturedImage = document.getElementById('captured-image');



// Access the webcam feed and display it in the video element
function openWebcam() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      videoFeed.srcObject = stream;
    })
    .catch(error => {
      console.error('Error accessing webcam:', error);
    });
}

function capturePicture() {
  // Check if the video stream is active
  if (videoFeed.srcObject && videoFeed.srcObject.active) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    // Set the canvas dimensions to match the video feed
    canvas.width = videoFeed.videoWidth;
    canvas.height = videoFeed.videoHeight;

    // Draw the current video frame onto the canvas
    context.drawImage(videoFeed, 0, 0, canvas.width, canvas.height);

    // Define the dimensions of the rectangle
    const rectangleWidth = canvas.width * 0.5; // Adjust the width as needed
    const rectangleHeight = canvas.height * 0.5; // Adjust the height as needed
    const rectangleX = (canvas.width - rectangleWidth) / 2;
    const rectangleY = (canvas.height - rectangleHeight) / 2;

    // Get the image data of the cropped rectangle
    const imageData = context.getImageData(rectangleX, rectangleY, rectangleWidth, rectangleHeight);

    // Create a new canvas for the cropped image
    const croppedCanvas = document.createElement('canvas');
    const croppedContext = croppedCanvas.getContext('2d');

    // Set the dimensions of the cropped canvas
    croppedCanvas.width = rectangleWidth;
    croppedCanvas.height = rectangleHeight;

    // Draw the cropped image onto the new canvas
    croppedContext.putImageData(imageData, 0, 0);

    // Convert the cropped canvas image to a data URL
    const croppedImageDataURL = croppedCanvas.toDataURL();

    // Create a form to send the captured image data to the server
    const form = new FormData();
    form.append('image', croppedImageDataURL);

    // Send the image data to the server using an AJAX request
    fetch('/capture', {
      method: 'POST',
      body: form
    })
      .then(response => {
        // Redirect to the capture.html page
        window.location.href = response.url;
      })
      .catch(error => {
        console.error('Error saving image:', error);
      });

    // Clean up the resources
    canvas.remove();
    croppedCanvas.remove();
  }
}


// Attach the capture function to the button click event
captureButton.addEventListener('click', function() {
  // Add CSS class to flash the button
  captureButton.classList.add('flash');
  setTimeout(function() {
    captureButton.classList.remove('flash');
  }, 300);

  capturePicture();
});
// Open the webcam on page load and create icons
document.addEventListener('DOMContentLoaded', function() {
  openWebcam();
});