// SOCKET
// let room_name = "{{ room_name | escapejs }}";
// let player_name = "{{ player_name | escapejs }}";

let wsStart = "ws";
if (window.location.protocol == "https:") {
  wsStart = "wss";
}
let chatSocket = new WebSocket(
  `${wsStart}://${window.location.host}/ws/mainapp/${room_name}/${player_name}/`
);

chatSocket.onclose = (e) => {
  console.error("Chat socket closed unexpectedly");
};

// GAME
const GAME_TIME = 30;
const COLOR_BOARD_BACKGROUND = 0xffb617;
let remainedTime = GAME_TIME;
let timeText;

let night;
let boss;

let scoreBoardPanel;
let table;
let createPanel;

let _this;

function attackAction() {
  // attack 후 idle
  night.play("night_attack").once("animationcomplete", () => {
    boss.play("boss_damaged").once("animationcomplete", () => {
      boss.play("boss_idle");
    });
    night.play("night_idle");
  });

  chatSocket.send(
    JSON.stringify({
      // type 필요
      type: "attack",
      message: "One player attacked",
    })
  );
}

function preload() {
  _this = this;
  this.load.scenePlugin(
    "rexuiplugin",
    "https://raw.githubusercontent.com/rexrainbow/phaser3-rex-notes/master/dist/rexuiplugin.min.js",
    "rexUI",
    "rexUI"
  );
  this.load.spritesheet("night", "/static/assets/night/NightBorne.png", {
    frameWidth: 80,
    frameHeight: 80,
  });
  this.load.spritesheet("boss", "/static/assets/boss/demon.png", {
    frameWidth: 288,
    frameHeight: 160,
  });
  //this.load.image('attack', "{% static 'images/attack.png' %}");
}

function create() {
  // night
  this.anims.create({
    key: "night_idle",
    frames: this.anims.generateFrameNumbers("night", { frames: range(0, 9) }),
    frameRate: 8,
    repeat: -1,
  });

  this.anims.create({
    key: "night_attack",
    frames: this.anims.generateFrameNumbers("night", {
      frames: range(46, 58),
    }),
    frameRate: 8,
    repeat: 0,
  });

  // boss
  this.anims.create({
    key: "boss_idle",
    frames: this.anims.generateFrameNumbers("boss", { frames: range(0, 6) }),
    frameRate: 8,
    repeat: -1,
  });

  this.anims.create({
    key: "boss_attack",
    frames: this.anims.generateFrameNumbers("boss", {
      frames: range(44, 59),
    }),
    frameRate: 8,
    repeat: 0,
  });

  this.anims.create({
    key: "boss_damaged",
    frames: this.anims.generateFrameNumbers("boss", {
      frames: range(66, 71),
    }),
    frameRate: 8,
    repeat: 0,
  });

  this.anims.create({
    key: "boss_die",
    frames: this.anims.generateFrameNumbers("boss", {
      frames: range(88, 88 + 22),
    }),
    frameRate: 8,
    repeat: 0,
  });

  // make characters
  night = this.add.sprite(window_width / 10, 370, "night");
  night.setScale(3);
  night.play("night_idle");

  boss = this.add.sprite(window_width - 100, 200, "boss");
  boss.setScale(3);
  boss.play("boss_idle");

  // 스코어보드
  createPanel = function (scene, data, state) {
    let sizer = scene.rexUI.add
      .sizer({
        orientation: "y",
        space: { item: 10 },
      })
      .add(
        createTable(scene, data, state, 2), // child
        { expand: true, key: state }
      );

    return sizer;
  };

  let createTable = function (scene, data, key, columns) {
    let capKey = key.charAt(0).toUpperCase() + key.slice(1);
    let title = scene.rexUI.add.label({
      orientation: "x",
      text: scene.add.text(0, 0, capKey, { color: "black" }),
    });

    // console.log(Math.floor((data.length - 1) / columns) + 1)
    table = scene.rexUI.add.gridSizer({
      column: columns,
      row: data.length,

      //rowProportions: 1,
      //columnProportions: 1,
      space: { column: 10, row: 10 },
      name: key, // Search this name to get table back
    });

    let item, r, c;

    // table header
    // item을 테이블에 배치
    for (let r = 0, cnt = data.length; r < cnt; r++) {
      item = data[r];
      for (let c = 0; c < 2; c++) {
        table.add(
          _this.add.text(0, 0, item[c], {
            fontFamily: "Arial",
            color: "white",
          }),
          c,
          r,
          "left",
          0,
          false
        );
      }
    }

    return scene.rexUI.add
      .sizer({
        orientation: "y",
        space: { left: 15, right: 10, top: 10, bottom: 10, item: 10 },
      })
      .addBackground(
        scene.rexUI.add
          .roundRectangle(0, 0, 0, 0, 0, undefined)
          .setStrokeStyle(2, COLOR_LIGHT, 1)
      )
      .add(
        title, // child
        0, // proportion
        "center", // align
        0, // paddingConfig
        true // expand
      )
      .add(
        table, // child
        1, // proportion
        "center", // align
        0, // paddingConfig
        false // expand
      );
  };

  scoreBoardPanel = this.rexUI.add
    .scrollablePanel({
      x: window_width / 2,
      y: window_height - window_height / 3 / 2 - 10,
      width: window_width / 1.5,
      height: window_height / 3,
      scrollMode: 0,

      background: this.rexUI.add.roundRectangle(
        0,
        0,
        0,
        0,
        0,
        COLOR_BOARD_BACKGROUND
      ),

      panel: {
        //child: createPanel(this, [[player_name, 0]], 'scoreBoard'),
        child: createTable(this, [["YOU", 0]], "scoreBoard", 2),
        mask: {
          padding: 0,
          // layer: this.add.layer()
        },
      },

      // scroller: true,
      scroller: {
        // pointerOutRelease: false
      },

      mouseWheelScroller: {
        focus: false,
        speed: 0.1,
      },

      space: {
        left: 10,
        right: 10,
        top: 10,
        bottom: 10,
        panel: 10,
        // slider: { left: 30, right: 30 },
      },
    })
    .layout();

  // add timer text
  timeText = _this.add.text(window_width / 2, 10, remainedTime, {
    fontFamily: "Arial",
    fontSize: 30,
    color: COLOR_LIGHT,
  });
  // console.log("timeText created");
}

// 게임 생성
let config = {
  type: Phaser.WEBGL,
  width: window_width,
  height: window_height,
  parent: "phaser-example",
  scene: {
    preload: preload,
    create: create,
  },
  backgroundColor: "#f2f7ff",
};

let game = new Phaser.Game(config);

// scoreBoard update
function updatetScoreBoard(message) {
  table.removeAll(true);
  table.resetGrid(2, message.length, 0, 0, {
    column: 10,
    row: 10,
  });

  for (let r = 0, cnt = message.length; r < cnt; r++) {
    item = message[r];
    for (let c = 0; c < 2; c++) {
      table.add(
        _this.add.text(0, 0, item[c], {
          fontFamily: "Arial",
          color: "white",
        }),
        {
          column: c,
          row: undefined,
          align: "left",
          expand: false,
        }
      );
    }
  }

  // re draw
  table.layout();
  scoreBoardPanel.layout();
}

let message = [];
// socket listener
chatSocket.onmessage = (e) => {
  let data = JSON.parse(e.data);
  message = data["message"];
  const type = data["type"];
  console.log(data);
  if (type == "attack") {
    // console.log('attack trigger');
    // attack 후 idle
    // night.play('night_attack').once('animationcomplete', () => {
    //    boss.play('boss_damaged').once('animationcomplete', () => {
    //        boss.play('boss_idle');
    //    });
    //    night.play("night_idle");
    //});

    // scoreBoard update
    updatetScoreBoard(message);
  } else if (type == "enter") {
    updatetScoreBoard(message);
  }
};

// face event listener
function move_mouth(da) {
  let tmp_dist = 0;

  if (da.length >= 2) {
    tmp_dist = Math.abs(parseInt(da.slice(-1)) - parseInt(da.slice(-2)));
  }
  return tmp_dist;
}

function partShot(str1, canvas) {
  // 스크린샷
  let image = canvas.toDataURL("image/jpeg");
  console.log(image);
  $.ajax({
    url: "/mainapp/api/face/",
    async: false,
    type: "POST",
    data: {
      face: image,
      csrfmiddlewaretoken: csrf_token,
    },
    datatype: "json",
    headers: { "X-CSRFToken": csrf_token },
  });
}

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
let total_distance = 0;
let workout_count = 0;
let capture_count_mouth = 0;
let capture_count_left = 0;
let capture_count_right = 0;
let workout = 200;

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
    canvas.getContext("2d").clearRect(0, 0, video.width, video.height);

    ///////////// 새로 추가
    let context = canvas.getContext("2d");
    let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    context.drawImage(video, 0, 0, video.width, video.height);
    src.data.set(context.getImageData(0, 0, video.width, video.height).data);
    // faceapi.draw.drawDetections(canvas, resizedDetections); // 주석
    // faceapi.draw.drawFaceLandmarks(canvas, resizedDetections); // 주석
    // faceapi.draw.drawFaceExpressions(canvas, resizedDetections); // 주석

    // x, y 좌표 어레이 생성
    let test_x = resizedDetections[0].landmarks._positions.map((e) => e._x);
    let test_y = resizedDetections[0].landmarks._positions.map((e) => e._y);

    x_arr.push(test_x);
    y_arr.push(test_x);

    // cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
    // 눈을 감았는지 떴는지를 opencv로 확인

    // cvtGray()
    // let src = new cv.Mat(canvas.height, canvas.width, cv.CV_8UC4);

    // let ctx = textToImg.getContext('2d');
    // let imgData = ctx.getImageData(0, 0, 720, 560);

    // let src = cv.matFromImageData(imgData);

    let x_left = (30 - (test_x[39] - test_x[36])) / 2;
    let x_right = (30 - (test_x[45] - test_x[42])) / 2;
    let y_left = (20 - (test_y[40] - test_y[37])) / 2;
    let y_right = (20 - (test_y[47] - test_y[43])) / 2;

    let x_df_eye_left_start = parseInt(test_x[36] - x_left);
    let x_df_eye_left_end = 30;
    // let x_df_eye_left_end = parseInt(test_x[39] + x_left) - x_df_eye_left_start

    let y_df_eye_left_start = parseInt(test_y[38] - y_left);
    let y_df_eye_left_end = 40;

    let x_df_eye_right_start = parseInt(test_x[42] - x_right);
    let x_df_eye_right_end = 30;

    let y_df_eye_right_start = parseInt(test_y[44] - y_right);
    let y_df_eye_right_end = 40;

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

    for (var i = 20; i <= 40; i++) {
      // 파라미터가 수정되었습니다 12, 20 --> 20, 40
      if (Array.isArray(right_matrix[i])) {
        right_count_check = getElNum(right_matrix[i], 255);
      }

      if (right_count_check <= 16) {
        // 값을 낮출수록 인식 기준이 하드해집니다
        // console.log('왼쪽 눈을 감음')
        right_count++;
      }
      if (Array.isArray(left_matrix[i])) {
        left_count_check = getElNum(left_matrix[i], 255);
      }

      if (left_count_check <= 10) {
        // 값을 낮출수록 인식 기준이 하드해집니다
        // console.log('오른쪽 눈을 감음')
        left_count++;
      }
    }
    //console.log("눈 감은 횟수", left_count_check, right_count_check);
    if (left_count >= 2 && left_count2 == 0) {
      // 값을 높일수록 인식 기준이 하드해집니다
      console.log(left_count, left_count2);
      attackAction();
      console.log("오른쪽 눈 스킬발동" + String(left_skill_count) + "번!");
      left_count2 = 1;
      left_skill_count++;
      // 수정된 부분
      if (capture_count_right <= 3) {
        // 웃긴 얼굴 캡쳐, 너무 많이 다운로드되어 일단은 저장개수를 변수 한개로 임시조정해두었습니다
        partShot(for_name, canvas);
        capture_count_right++;
      }
    }
    if (left_count < 2) {
      left_count2 = 0;
    }
    // 수정된 부분
    if (right_count >= 2 && right_count2 == 0) {
      // 값을 높일수록 인식 기준이 하드해집니다
      attackAction();
      console.log("왼쪽 눈 스킬발동" + String(right_skill_count) + "번!");
      right_count2 = 1;
      right_skill_count++;
      // 수정된 부분
      if (capture_count_left <= 3) {
        partShot(for_name, canvas);
        capture_count_left++;
      }
    }
    if (right_count < 2) {
      right_count2 = 0;
    }

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

    total_distance += move_mouth(distance_array);
    if (
      total_distance % workout <= 50 &&
      total_distance / workout >= 1 &&
      workout_count == 0
    ) {
      console.log("운동량" + total_distance + "돌파! 구강이 튼튼하시군요");
      workout_count = 1;
    }
    if (total_distance % workout >= 50 && total_distance / workout >= 1) {
      workout_count = 0;
    }

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
      if (capture_count_mouth <= 3) {
        partShot(for_name, canvas);
        capture_count_mouth++;
      }
      count2++;
      mouth_skill_count++;
    }
  }, 100); // 현재 0.1초

  // 비디오가 play 되면
  // game timer
  // timer start
  setTimeout(() => {
    for (let second = 0; second < GAME_TIME; second++) {
      setTimeout(() => {
        // console.log("timeText timer fired");
        remainedTime--;
        timeText.setText(remainedTime);
      }, 1000 * second);

      // end of game
      setTimeout(() => {
        night.stop();
        video.pause();
        boss.play("boss_die").once("animationcomplete", () => {
          const state = {
            left_eye: left_skill_count,
            right_eye: right_skill_count,
            mouth: mouth_skill_count,
          };

          showFinalScore(message);
        });
      }, 1000 * GAME_TIME + 1000);
    }

    document.querySelector(".mask").style.visibility = "hidden";
  }, 5000); // 딜레이로 5초 뒤 시작
});

function showFinalScore(scoreData) {
  tableElement = "";
  for (let row = 0; row < scoreData.length; row++) {
    const oneScore = scoreData[row];
    tableElement += `<tr>
                      <th>${oneScore[0]}</th>
                      <th>${oneScore[1]}</th>
                    </tr>`;
  }

  cuteAlert({
    type: "success",
    title: "GAME END",
    message: `당신은 ${
      scoreData.map((arr) => arr[0]).indexOf(player_name) + 1
    }등을 하셨습니다`,
    img: `<table class='table'>
            <thead class='table-dark'>
              <tr>
                <th>player</th>
                <th>score</th>
              </tr>
            </thead>
            <tbody>
              ${tableElement}
            </tbody>
          </table>`,
    buttonText: "NEXT",
  }).then(() => {
    window.location.href = `/mainapp/result?left_eye=${left_skill_count}&right_eye=${right_skill_count}&mouth=${mouth_skill_count}`;
  });
}
