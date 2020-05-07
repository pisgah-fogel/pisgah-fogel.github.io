#include <irrlicht/irrlicht.h>

using namespace irr;

#ifdef _MSC_VER
#pragma comment(lib, "Irrlicht.lib")
#endif


class MyEventReceiver : public IEventReceiver
{
public:

    MyEventReceiver(scene::ISceneNode* terrain, scene::ISceneNode* skybox, scene::ISceneNode* skydome, bool* needToExit) :
        Terrain(terrain), Skybox(skybox), Skydome(skydome), showBox(true), showDebug(false)
    {
        Skybox->setVisible(showBox);
        Skydome->setVisible(!showBox);
        ptrExit = needToExit;
    }

    bool OnEvent(const SEvent& event)
    {
        // check if user presses the key 'W' or 'D'
        if (event.EventType == irr::EET_KEY_INPUT_EVENT && !event.KeyInput.PressedDown)
        {
            switch (event.KeyInput.Key)
            {
            case irr::KEY_KEY_W: // switch wire frame mode
                Terrain->setMaterialFlag(video::EMF_WIREFRAME,
                        !Terrain->getMaterial(0).Wireframe);
                Terrain->setMaterialFlag(video::EMF_POINTCLOUD, false);
                return true;
            case irr::KEY_KEY_P: // switch wire frame mode
                Terrain->setMaterialFlag(video::EMF_POINTCLOUD,
                        !Terrain->getMaterial(0).PointCloud);
                Terrain->setMaterialFlag(video::EMF_WIREFRAME, false);
                return true;
            case irr::KEY_KEY_D: // toggle detail map
                Terrain->setMaterialType(
                    Terrain->getMaterial(0).MaterialType == video::EMT_SOLID ?
                    video::EMT_DETAIL_MAP : video::EMT_SOLID);
                return true;
            case irr::KEY_KEY_S: // toggle skies
                showBox=!showBox;
                Skybox->setVisible(showBox);
                Skydome->setVisible(!showBox);
                return true;
            case irr::KEY_KEY_X: // toggle debug information
                showDebug=!showDebug;
                Terrain->setDebugDataVisible(showDebug?scene::EDS_BBOX_ALL:scene::EDS_OFF);
                return true;
            case irr::KEY_KEY_Q: // quit
                *ptrExit = true;
                return true;
            default:
                break;
            }
        }

        return false;
    }

private:
    scene::ISceneNode* Terrain;
    scene::ISceneNode* Skybox;
    scene::ISceneNode* Skydome;
    bool showBox;
    bool showDebug;
    bool* ptrExit;
};