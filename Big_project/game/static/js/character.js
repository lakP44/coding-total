import Phaser from 'phaser'

  
function preload ()
{
    //bgs
    this.load.image('bg', 'UIUX/background/BG.png');

    //bodies
    this.load.image('body', 'UIUX/character/char_front.png');

    //hairs
    this.load.image('hair1','UIUX/custome/hairs/hair1.png');
    this.load.image('hair2', 'UIUX/custome/hairs/hair2.png');

    //tops
    this.load.image('top1','UIUX/custome/tops/top1.png');
    this.load.image('top2', 'UIUX/custome/tops/top2.png');

    //bottoms
    //추후추가
    // this.load.image('bottom1','UIUX/custome/bottoms/bottom1.png');
    // this.load.image('bottom2', 'UIUX/custome/botoms/bottom2.png');

    //shoes
    //추후추가
    // this.load.image('shoes1', 'UIUX/custome/shoes/shoes1.png');
    // this.load.image('shoes2', 'UIUX/custome/shoes/shoes2.png');


    //weapons
    //추후추가
    // this.load.image('weapon1', 'UIUX/custome/weapons/weapon1.png');
    // this.load.image('weapon2', 'UIUX/custome/weapons/weapon2.png');


    //UI
    this.load.image('hairtxt', 'UIUX/ui/헤어버튼.png');
    this.load.image('toptxt', 'UIUX/ui/상의버튼.png');
    this.load.image('bottomtxt', 'UIUX/ui/하의버튼.png');
    this.load.image('shoestxt', 'UIUX/ui/신발버튼.png');
    this.load.image('weapontxt', 'UIUX/ui/무기버튼.png');
    this.load.image('leftArrow', 'UIUX/ui/왼쪽버튼.png');
    this.load.image('rightArrow', 'UIUX/ui/오른쪽버튼.png');

}


function create ()
{

    tiles = this.physics.add.staticGroup();
    arrows = this.physics.add.staticGroup();
    smalltiles = this.physics.add.staticGroup();
    text = this.physics.add.staticGroup();

this.add.image(500,300,'bg');

    //UI options
    bodytxt = text.create(500, 170, 'bodytext').setInteractive();
    hairtxt = text.create(500, 220, 'hairtxt').setInteractive();
    toptxt = text.create(530, 270, 'toptxt').setInteractive();
    bottomtxt = text.create(500, 320, 'bottomtxt').setInteractive();
    shoestxt = text.create(500, 370, 'shoestxt').setInteractive();
    weapontxt = text.create(500, 420, 'weapontxt').setInteractive();
    leftArrow = arrows.create(650,290, 'leftarrow').setInteractive();
    rightArrow = arrows.create(950,290, 'rightarrow').setInteractive();


    //colour tile objects
    red = smalltiles.create(695, 470, 'smalltile').setTint(0x85251B).setInteractive();      
    orange = smalltiles.create(725, 470, 'smalltile').setTint(0x874E0F).setInteractive();
    yellow = smalltiles.create(755, 470, 'smalltile').setTint(0xB2B037).setInteractive();
    green = smalltiles.create(785, 470, 'smalltile').setTint(0x4C7940).setInteractive();
    lightblue = smalltiles.create(815, 470, 'smalltile').setTint(0x7F9293).setInteractive();        
    darkblue = smalltiles.create(845, 470, 'smalltile').setTint(0x383A4B).setInteractive();
    purple = smalltiles.create(875, 470, 'smalltile').setTint(0x6F5F78).setInteractive();
    pink = smalltiles.create(905, 470, 'smalltile').setTint(0xD6A16B).setInteractive();     
    
    //player layers
    //playershirt;
    //playerpants;
    //playershoes;
    //playeraccessories;
    //playerbg;


    //MENU ICONS

    //hairs
    hairicon1 = this.add.image(735,185, 'hair1').setScale(0.35).setInteractive();
    hairicon2 = this.add.image(812,185, 'hair2').setScale(0.35).setInteractive();
    // hairicon3 = this.add.image(893,185, 'hair3').setScale(0.35).setInteractive();


    //MOUSE INTERACTIONS

    //click colour tiles
    red.on('pointerdown', function (pointer, red) { colour = 0x85251B; });
    orange.on('pointerdown', function (pointer, orange) { colour = 0x874E0F;  });
    yellow.on('pointerdown', function (pointer, yellow){ colour = 0xB2B037; });
    green.on('pointerdown', function(pointer, green){ colour = 0x4C7940; });
    lightblue.on('pointerdown', function(pointer, lightblue){ colour = 0x7F9293; });
    darkblue.on('pointerdown', function(pointer, darkblue){ colour = 0x383A4B;  });
    purple.on('pointerdown', function(pointer, purple){ colour = 0x6F5F78;  });
    pink.on('pointerdown', function(pointer, pink){ colour = 0xD6A16B; });
    
    //click menu text
    bodytxt.on('pointerdown', function (pointer, bodytxt) { selection = 1; page =0; });                
    hairstxt.on('pointerdown', function (pointer, hairstxt) { selection = 2; page = 0; playerhair });   
    toptxt.on('pointerdown', function (pointer, toptxt) { selection = 3; page = 0; playertop });   
    bottomtxt.on('pointerdown', function (pointer, bottomtxt) { selection = 4; page = 0; playerbottom });   
    shoestxt.on('pointerdown', function (pointer, shoestxt) { selection = 5; page = 0; playershoes });   
    weapontxt.on('pointerdown', function (pointer, weapontxt) { selection = 6; page = 0; playerweapon });   
    

    //click item icons
    hairicon1.on('pointerdown', function (pointer, hairicon1){ });
    hairicon2.on('pointerdown', function (pointer, hairicon2){ });
    hairicon3.on('pointerdown', function (pointer, hairicon3){ });

    //click arrows
    leftArrow.on('pointerdown', function(pointer, leftArrow){ page -= 1; });
    rightArrow.on('pointerdown', function(pointer, rightArrow){ page += 1; });

    //ANIMATIONS
    // var keys = ['cat', 'pupil', 'faceblink', 'gothblink', 'shiftyblink'];
    // var spritesheets = ['catbody','cateyes', 'catface', 'catfacegoth', 'catfaceshifty'];

    // for(var i = 0; i < keys.length; i++){
    //     this.anims.create({
    //         key: keys[i],
    //         frames: this.anims.generateFrameNumbers(spritesheets[i], { start: 0, end: 13 }),
    //         frameRate: 10,
    //         repeat: -1
    //     });
    // }
}
//end create





//custom functions

//helper function, sets individual icon to active/visible to inactive/invisible
function setActivity(icon, bool){
    icon.input.enabled = bool;
    icon.setVisible(bool);
}


//Sets each item icon in an array to active/visible or inactive/invisible
function setAllActivity(array, bool){    
    for(var i = 0; i < array.length; i++){
        setActivity(array[i], bool);
    }
}

//Displays the desired item menu icons as listed in the current page
function setJustOne(all, desired, page){
    //i = icon category index
    for(var i = 0; i < all.length; i++){
        //j = array for each page of icons
        for(var j = 0; j < all[i].length; j++){
            if(all[i] != desired || j != page){
                setAllActivity(all[i][j], false);
            }
            if(all[i] == desired && j == page){
                setAllActivity(all[i][j], true);
            }
        }
    }
}


//tints text icon and clears tint from all other text icons
function selected(icon, array){
    for(var i = 0; i < array.length; i++){
        if(array[i] != icon){
            array[i].clearTint()
        }
        if(array[i] == icon){
            array[i].setTint(0xff0000);
        }
    }
}

//plays the animation key given to the player body
function playBody(bodyKey){
    player.anims.play(bodyKey, true);
}

//plays the animation key given to the player's face
function playFace(facekey){
    playerface.anims.play(facekey, true);
    playereyes.anims.play('pupil', true);
}

//helper function for menuOptions(). Ensures page index does not go out of bounds.
function pageCtrl(page, max){
    if(page >= max){
        this.page = max;
    }
    if (page <= 0){
        this.page = 0;
    }
}


//When user clicks any text section it triggers displaying of relevant item icons.  
function menuOptions(selection){
    
    //icon arrays 
    //2D, bodyIcons[0] = first page array, bodyIcons[0][0] = first item on first page 
    var bodyIcons = [ [], [], [] ];
    var hairIcons = [[hairicon1, hairicon2, hairicon3], [], [] ];
    var topIcons = [ [], [], [] ];
    var bottomIcons = [ [], [], []];
    var shoesIcons= [ [], [], []];
    var weaponIcons= [ [], [], [] ];

    //3D array 
    //allIcons[0] = bodyIcons, allIcons[0][0] = First page, allIcons [0][0][0] = first elem in first page 
    var allIcons = [bodyIcons, hairIcons, topIcons, bottomIcons, shoesIcons, weaponIcons]; 

    //just an array of interactive text objects.
    var textIcons = [bodytxt, hairtxt, toptxt, bottomtxt, shoestxt, weapontxt];



    //body selection
    if(selection == 1){  
        currentobj = player;
        selected(bodytxt, textIcons);
        pageCtrl(page, bodyIcons.length);
        console.log('selection 1 page:' + page);
        setJustOne(allIcons, bodyIcons, page);
    }
    //hair selection
    if(selection == 2){
        currentobj = playehair;
        selected(hairtxt, textIcons);
        pageCtrl(page, hairIcons.length);
        console.log('selection 2 page:' + page);
        setJustOne(allIcons, hairIcons, page);
    }
    //top section
    if(selection == 3){
        currentobj = top;
        selected(toptxt, textIcons);
        pageCtrl(page, topIcons.length);
        console.log('selection 3 page:' + page);
        setJustOne(allIcons, topIcons, page);
    }
    //bottom section
    if(selection == 4){
        //currentobj = bottom;
        selected(bottomtxt, textIcons);
        pageCtrl(page, bottomIcons.length);
        console.log('selection 4 page:' + page);
        setJustOne(allIcons, bottomIcons, page);
    }
    //shoes section
    if(selection == 5){
        //currentobj = shoes;
        selected(shoestxt, textIcons);
        pageCtrl(page, shoesIcons.length);
        console.log('selection 5 page:' + page);
        setJustOne(allIcons, shoesIcons, page);
    }
    //weapon section
    if(selection == 6){
        //currentobj = weapon;
        selected(weapontxt, textIcons);
        pageCtrl(page, weaponIcons.length);
        console.log('selection 6 page:' + page);
        setJustOne(allIcons, weaponIcons, page);
    }
}

var colour = 0x85251B;
var selection = 1;
var currentobj;
// facekey = 'shiftyblink';
// bodyKey = 'cat'
var page = 0;

//Game Main
function update ()
{ 
    //sprite layers
    // playBody(bodyKey);                    //body
    // playFace(facekey);                    //face/ eyes

    menuOptions(selection);               //select section
    currentobj.setTint(colour);           //tint section
    
}



// const config = {
//     type: Phaser.AUTO,
//     width: 600,
//     height: 600,
//     physics: {
//         default: 'arcade',
//         arcade: {
//             debug: false,
//             gravity: {
//                 y: 0
//             }
//         }
//     },
//     backgroundColor: '#38ab5b',
//     scene: {
//       preload: preload,
//       create: create,
//       update:update,
//     },
//     scale: {
//         mode: Phaser.Scale.ScaleModes.FIT
//     }
//   }
//   var game =  new Phaser.Game(config)