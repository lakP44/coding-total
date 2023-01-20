// 수정된 부분
function move_mouth(da) {

  let tmp_dist = 0

  if (da.length >= 2) {
      tmp_dist = Math.abs(parseInt(da.slice(-1)) - parseInt(da.slice(-2)))
  }
  return tmp_dist
}

function PartShot(str1) {
  //특정부분 스크린샷
  html2canvas(document.getElementById("video"))
  //id container 부분만 스크린샷
      .then(function (canvas) {
          //jpg 결과값
          drawImg(canvas.toDataURL('image/jpeg'));
          //이미지 저장
          saveAs(canvas.toDataURL(), 'face_org'+String(str1)+'.jpg');
      }).catch(function (err) {
          console.log(err);
      });
}

function saveAs(uri, filename) {
  var link = document.createElement("a");
  if (typeof link.download === "string") {
    link.href = uri;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } else {
    window.open(uri);
  }
}

function drawImg(imgData) {
  // console.log(imgData);
  //imgData의 결과값을 console 로그롤 보실 수 있습니다.
  return new Promise(
    function reslove() {
      //내가 결과 값을 그릴 canvas 부분 설정
      var canvas = document.getElementById("canvas");
      var ctx = canvas.getContext("2d");
      //canvas의 뿌려진 부분 초기화
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      var imageObj = new Image();
      imageObj.onload = function () {
        ctx.drawImage(imageObj, 0, 0);
        //canvas img를 그리겠다.
      };
      imageObj.src = imgData;
      //그릴 image데이터를 넣어준다.
    },
    function reject() {}
  );
}
// 수정된 부분


var distance_array = [];
var count = 0;
var count2 = 0;
var mouth_skill_count = 0;
var left_skill_count = 0;
var right_skill_count = 0;
let left_count2 = 0;
let right_count2 = 0;
var time_delay = 0;
let for_name = 0;
// 수정된 부분
let total_distance = 0;
let workout_count = 0;
let capture_count_mouth = 0;
let capture_count_left = 0;
let capture_count_right = 0;
let workout = 200;
// 수정된 부분
const getElNum = (arr, el) => arr.reduce((ac, v) => ac + (v === el), 0);
x_arr = [];
y_arr = [];

video.addEventListener("play", () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  canvas.id = "match-dimension";
  document.body.append(canvas);

  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks();
    // .withFaceExpressions(); // 주석
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    let cap = new cv.VideoCapture(video); // 12-28 수정된부분
    // canvas.getContext("2d").clearRect(0, 0, video.width, video.height);

    ///////////// 새로 추가
    //     let context = canvas.getContext("2d");
    let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    cap.read(src); // 12-28 수정된부분
    //context.drawImage(video, 0, 0, video.width, video.height);
    //     src.data.set(context.getImageData(0, 0, video.width, video.height).data);
    // faceapi.draw.drawDetections(canvas, resizedDetections); // 주석
    // faceapi.draw.drawFaceLandmarks(canvas, resizedDetections); // 주석
    // faceapi.draw.drawFaceExpressions(canvas, resizedDetections); // 주석

    // x, y 좌표 어레이 생성
    let test_x = resizedDetections[0].landmarks._positions.map((e) => e._x);
    let test_y = resizedDetections[0].landmarks._positions.map((e) => e._y);

    x_arr.push(test_x);
    y_arr.push(test_x);
    
    // 12-28 수정된 부분
    let x_df_eye_left_start = parseInt(test_x[36] - 5);
    let x_df_eye_left_end = 20;
    // let x_df_eye_left_end = parseInt(test_x[39] + x_left) - x_df_eye_left_start

    let y_df_eye_left_start = parseInt(test_y[38] - 2);
    let y_df_eye_left_end = 15; // 파라미터가 수정되었습니다 40 --> 35

    let x_df_eye_right_start = parseInt(test_x[42] - 5);
    let x_df_eye_right_end = 20;

    let y_df_eye_right_start = parseInt(test_y[44] - 2);
    let y_df_eye_right_end = 15; // 파라미터가 수정되었습니다 40 --> 35
    // 수정된 부분
    
    // You can try more different parameters
    let rect_left = new cv.Rect(
      x_df_eye_left_start,
      y_df_eye_left_start,
      x_df_eye_left_end,
      y_df_eye_left_end
    );
    dst_left = src.roi(rect_left);

    let rect_right = new cv.Rect(
      x_df_eye_right_start,
      y_df_eye_right_start,
      x_df_eye_right_end,
      y_df_eye_right_end
    );
    dst_right = src.roi(rect_right);

    cv.cvtColor(dst_left, dst_left, cv.COLOR_RGBA2GRAY);
    cv.cvtColor(dst_right, dst_right, cv.COLOR_RGBA2GRAY);

    cv.threshold(dst_left, dst, 0, 255, cv.THRESH_OTSU);
    let left_array = JSON.parse("[" + dst.data.toString() + "]");

    cv.threshold(dst_right, dst, 0, 255, cv.THRESH_OTSU);
    let right_array = JSON.parse("[" + dst.data.toString() + "]");

    let left_matrix = listToMatrix(left_array, 30);
    let right_matrix = listToMatrix(right_array, 30);

    let left_count = 0;
    let right_count = 0;
    let left_count_check;
    let right_count_check;

    // 수정된 부분
    for (var i = 3; i <= 15; i++) { // 파라미터가 수정되었습니다 20, 40 --> 2, 15
      if (Array.isArray(right_matrix[i])) {
        right_count_check = getElNum(right_matrix[i], 255);
      }

      if (right_count_check <= 3) { // 값을 낮출수록 인식 기준이 하드해집니다
        // console.log('왼쪽 눈을 감음')
        right_count++;
      }
      if (Array.isArray(left_matrix[i])) {
        left_count_check = getElNum(left_matrix[i], 255);
      }

      if (left_count_check <= 3) { // 값을 낮출수록 인식 기준이 하드해집니다
        // console.log('오른쪽 눈을 감음')
        left_count++;
      }
    }
    console.log("255 횟수 체크: ", left_count, right_count);
    if (left_count >= 2 && left_count2 == 0) { // 값을 높일수록 인식 기준이 하드해집니다
      attackAction();
      console.log("오른쪽 눈 스킬발동" + String(left_skill_count) + "번!");
      left_count2 = 1;
      left_skill_count++;
      // 수정된 부분
      if (capture_count_right <= 3) { // 웃긴 얼굴 캡쳐, 너무 많이 다운로드되어 일단은 저장개수를 변수 한개로 임시조정해두었습니다
        PartShot(for_name)
        capture_count_right++
        }
      };
      if (left_count < 2) {
        left_count2 = 0
      }
      // 수정된 부분
    if (right_count >= 2 && right_count2 == 0) { // 값을 높일수록 인식 기준이 하드해집니다
      attackAction();
      console.log("왼쪽 눈 스킬발동" + String(right_skill_count) + "번!");
      right_count2 = 1;
      right_skill_count++;
      // 수정된 부분
      if (capture_count_left <= 3) {
        PartShot(for_name)
        capture_count_left++
        }
    }
    if (right_count < 2) {
      right_count2 = 0
    }
      // 수정된 부분
    
    src.delete();
    dst.delete();
    dst_left.delete();
    dst_right.delete();

    // 입벌림을 감지하는 부분
    let test_x_29 = test_x[29];
    let test_x_57 = test_x[57];

    let test_y_29 = test_y[29];
    let test_y_57 = test_y[57];

    let x_sub = test_x_57 - test_x_29;
    let y_sub = test_y_57 - test_y_29;

    let distance = (x_sub ** 2 + y_sub ** 2) ** (1 / 2);

    distance_array.push(distance);
    
    // 수정된 부분
    total_distance += move_mouth(distance_array)
    if (total_distance % workout <= 50 &&  total_distance / workout >= 1 && workout_count == 0){
    console.log('운동량' + total_distance + '돌파! 구강이 튼튼하시군요')
    workout_count = 1
    }
    if (total_distance % workout >= 50 &&  total_distance / workout >= 1){
    workout_count = 0}
    // 수정된 부분
    
    if (distance >= distance_array[0] * 1.4) {
      // console.log( " 입벌림 " );
      count++;
    } else {
      // console.log( " 입닫음 " );
      count = 0;
      count2 = 0;
    }
    if (count == 1 && count2 == 0) {
      attackAction();
      console.log("입 스킬발동" + String(mouth_skill_count) + "번!");
      // 수정된 부분
      if (capture_count_mouth <= 3){
        PartShot(for_name)
        capture_count_mouth++ 
      }
      // 수정된 부분
      count2++;
      mouth_skill_count++;
    }
  }, 100); // 현재 0.1초
});
