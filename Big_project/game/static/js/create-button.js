const COLOR_LIGHT = 0x6b5ce0;

function createButton(scene, key) {
  return scene.rexUI.add.label({
    background: scene.rexUI.add.roundRectangle(
      0,
      0,
      0,
      0,
      40,
      COLOR_LIGHT,
      0.8
    ),
    icon: scene.add.image(0, 0, key),
    iconSize: 40,
    align: "center",
  });
}
