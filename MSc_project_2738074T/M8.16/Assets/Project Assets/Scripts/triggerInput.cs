using System.Collections;
using System.Diagnostics;
using UnityEngine;
using Valve.VR;
using ViveSR.anipal.Eye; // 删除 MyProject.Scripts

public class triggerInput : MonoBehaviour
{
    public StimulusGenerator stimulusGenerator;
    public EyeTracking eyeTracking;

    private SteamVR_Behaviour_Pose controllerPose;
    private SteamVR_Input_Sources inputSource;
    private SteamVR_Action_Boolean backTriggerAction;
    private SteamVR_Action_Boolean Teleport;

    private bool triggerPressed = false;

    private void Awake() // sets up controls and disables eyetracking and stimulusgenerator until re-enabled in update
    {
        controllerPose = GetComponentInParent<SteamVR_Behaviour_Pose>();
        inputSource = controllerPose.inputSource;

        backTriggerAction = SteamVR_Actions.default_InteractUI;

        Teleport = SteamVR_Actions.default_Teleport;

        if (eyeTracking != null)
            eyeTracking.enabled = false;

        if (stimulusGenerator != null)
            stimulusGenerator.enabled = false;
    }

    private void Update() // called each frame, if trigger down, signal is sent to stimulusgenerator
    {
        if (backTriggerAction[inputSource].stateDown)
        {
            if (!triggerPressed)
            {
                triggerPressed = true;

                if (stimulusGenerator != null)
                {
                    stimulusGenerator.OnTriggerPulled();
                }
            }
        }
        else if (backTriggerAction[inputSource].stateUp)
        {
            triggerPressed = false;
        }

        if (Teleport[inputSource].stateDown)
        {
            StartCoroutine(ActivateScriptsAfterDelay(5f));
        }
    }

    private IEnumerator ActivateScriptsAfterDelay(float delay) // used to enable scripts at start using centre button
    {
        yield return new WaitForSeconds(delay);

        if (eyeTracking != null && !eyeTracking.enabled)
        {
            eyeTracking.enabled = true;
        }

        yield return new WaitForSeconds(0.01f);

        if (stimulusGenerator != null && !stimulusGenerator.enabled)
        {
            stimulusGenerator.enabled = true;
        }
    }
}
