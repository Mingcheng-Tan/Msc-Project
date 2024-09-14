using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using Valve.VR.Extras;

public class InputHandler : MonoBehaviour
{
    public SceneTransitionManager sceneTransitionManager;
    public SteamVR_LaserPointer laserPointer;

    void Awake()
    {
        laserPointer.PointerClick += PointerClick;
    }

    public void PointerClick(object sender, PointerEventArgs e)
    {
        if (e.target.name == "Test")
        {
            sceneTransitionManager.GoToScene(1); // useful function that allows user to traverse scenes. Scene id's can be found in file-> build settings
        }
        if (e.target.name == "Test_NoFeedback")
        {
            sceneTransitionManager.GoToScene(2); // useful function that allows user to traverse scenes. Scene id's can be found in file-> build settings
        }
    }
}