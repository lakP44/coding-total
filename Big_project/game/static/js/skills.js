import Phaser from 'phaser'

var config = {
    width: 200,
    height: 600,
    backgroundColor: 0x000000,
}

var game = new Phaser.Game(config);

this.scene.add('Main');
this.scene.start('Main');

export default class skills extends Phaser.Scene {
    constructor() {
        super("bootGame");
    }
  }

  create() {
    this.add.text(20,20,"스킬관리창입니다");
    this.scene.start("playGame");
  }