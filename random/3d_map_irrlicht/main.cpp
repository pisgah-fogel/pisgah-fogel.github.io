#include <irrlicht/irrlicht.h>
#include "MyEventReceiver.h"

using namespace irr;
using namespace core;
using namespace scene;
using namespace video;
using namespace io;
using namespace gui;
#ifdef _IRR_WINDOWS_
#pragma comment(lib, "Irrlicht.lib")
#pragma comment(linker, "/subsystem:windows /ENTRY:mainCRTStartup")
#endif

int main()
{
	// video::EDT_OPENGL
    // video::EDT_DIRECT3D9
    // video::EDT_DIRECT3D8
    // video::EDT_BURNINGSVIDEO
    // video::EDT_SOFTWARE
    // video::EDT_NULL
	IrrlichtDevice *device =
		createDevice( video::EDT_OPENGL, dimension2d<u32>(640, 480), 16,
				false, false, false, 0);

	if (!device)
		return 1;
	device->setWindowCaption(L"Hello World! - Irrlicht Engine Demo");
	IVideoDriver* driver = device->getVideoDriver();
	ISceneManager* smgr = device->getSceneManager();
	IGUIEnvironment* guienv = device->getGUIEnvironment();

	driver->setTextureCreationFlag(video::ETCF_ALWAYS_32_BIT, true);

	guienv->addStaticText(L"Press 'W' to change wireframe mode\nPress 'D' to toggle detail map\nPress 'S' to toggle skybox/skydome",
			rect<s32>(380,10,620,62), false);

	//IAnimatedMeshSceneNode* node = smgr->addOctreeSceneNode(IAnimatedMesh *mesh, SceneNode *parent = 0,s32 id = -1,s32 minimalPolysPerNode = 512,bool alsoAddIfMeshPointerZero = false) 	

	guienv->addImage(driver->getTexture("media/irrlichtlogo2.png"), core::position2d<s32>(10,10));
	guienv->getSkin()->setFont(guienv->getFont("media/fontlucida.png"));

	//smgr->addCameraSceneNode(0, vector3df(0,30,-40), vector3df(0,5,0));
	scene::ICameraSceneNode* camera = smgr->addCameraSceneNodeFPS(0,100.0f,1.2f);

	camera->setPosition(core::vector3df(2700*2,255*2,2600*2));
    camera->setTarget(core::vector3df(2397*2,343*2,2700*2));
    camera->setFarValue(42000.0f);

	device->getCursorControl()->setVisible(false);

    scene::ITerrainSceneNode* terrain = smgr->addTerrainSceneNode(
        "media/terrain-heightmap.bmp",
        0,                  // parent node
        -1,                 // node id
        core::vector3df(0.f, 0.f, 0.f),     // position
        core::vector3df(0.f, 0.f, 0.f),     // rotation
        core::vector3df(40.f, 4.4f, 40.f),  // scale
        video::SColor ( 255, 255, 255, 255 ),   // vertexColor
        5,                  // maxLOD
        scene::ETPS_17,             // patchSize
        4                   // smoothFactor
        );

    terrain->setMaterialFlag(video::EMF_LIGHTING, false);

    terrain->setMaterialTexture(0,
            driver->getTexture("media/terrain-texture.jpg"));
    terrain->setMaterialTexture(1,
            driver->getTexture("media/detailmap3.jpg"));
    
    terrain->setMaterialType(video::EMT_DETAIL_MAP);

    terrain->scaleTexture(1.0f, 20.0f);

	// create triangle selector for the terrain 
    scene::ITriangleSelector* selector
        = smgr->createTerrainTriangleSelector(terrain, 0);
    terrain->setTriangleSelector(selector);

    // create collision response animator and attach it to the camera
    scene::ISceneNodeAnimator* anim = smgr->createCollisionResponseAnimator(
        selector, camera, core::vector3df(60,100,60),
        core::vector3df(0,0,0),
        core::vector3df(0,50,0));
    selector->drop();
    camera->addAnimator(anim);
    anim->drop();

	driver->setTextureCreationFlag(video::ETCF_CREATE_MIP_MAPS, false);

    scene::ISceneNode* skybox=smgr->addSkyBoxSceneNode(
        driver->getTexture("media/irrlicht2_up.jpg"),
        driver->getTexture("media/irrlicht2_dn.jpg"),
        driver->getTexture("media/irrlicht2_lf.jpg"),
        driver->getTexture("media/irrlicht2_rt.jpg"),
        driver->getTexture("media/irrlicht2_ft.jpg"),
        driver->getTexture("media/irrlicht2_bk.jpg"));
    scene::ISceneNode* skydome=smgr->addSkyDomeSceneNode(driver->getTexture("media/skydome.jpg"),16,8,0.95f,2.0f);

    driver->setTextureCreationFlag(video::ETCF_CREATE_MIP_MAPS, true);

	bool needToExit = false;
	MyEventReceiver receiver(terrain, skybox, skydome, &needToExit);
    device->setEventReceiver(&receiver);

	while(device->run() && !needToExit)
	{
		driver->beginScene(true, true, 0);

		smgr->drawAll();
		guienv->drawAll();

		driver->endScene();
	}
	device->drop();

	return 0;
}
