using System.IO;
using System.Runtime.InteropServices;
using UnityEngine;
using ViveSR.anipal.Eye;

public class EyeTracking : MonoBehaviour
{
    public GameObject StimulusObject;
    private LineRenderer gazeRayRenderer;
    private readonly float MaxDistance = 20;
    private static EyeData eyeData = new EyeData();
    private bool eye_callback_registered = false;
    private StreamWriter outputStream;
    private string outputPath = "Data/Logs/EyeTrackingData.txt";
    private readonly GazeIndex[] GazePriority = new GazeIndex[] { GazeIndex.COMBINE, GazeIndex.LEFT, GazeIndex.RIGHT };
    private float startTime; // this will be used to takeaway script start time from scene start time to get actual time when script was enabled.
    private bool looking_at_stim = false;

    void Start()
    {
        gazeRayRenderer = GetComponent<LineRenderer>();
        startTime = Time.time;
    }

    public void SetOutputPath(string path)
    {
        outputPath = Path.Combine(path, "EyeTrackingData.txt");
        if (outputStream != null)
        {
            outputStream.Close();
        }
        outputStream = new StreamWriter(outputPath, true);
        outputStream.WriteLine($"{StimulusObject.name}");
    }


    private void Update() // called each frame, firstly checks eyetracking status is okay before logging any contact of ray gaze to raw eyetrackingdata.txt, also calls centralstimulus script to change colour
    {
        if (SRanipal_Eye_Framework.Status != SRanipal_Eye_Framework.FrameworkStatus.WORKING &&
            SRanipal_Eye_Framework.Status != SRanipal_Eye_Framework.FrameworkStatus.NOT_SUPPORT) return;

        if (SRanipal_Eye_Framework.Instance.EnableEyeDataCallback == true && !eye_callback_registered)
        {
            SRanipal_Eye.WrapperRegisterEyeDataCallback(Marshal.GetFunctionPointerForDelegate((SRanipal_Eye.CallbackBasic)EyeCallback));
            eye_callback_registered = true;
        }
        else if (!SRanipal_Eye_Framework.Instance.EnableEyeDataCallback && eye_callback_registered)
        {
            SRanipal_Eye.WrapperUnRegisterEyeDataCallback(Marshal.GetFunctionPointerForDelegate((SRanipal_Eye.CallbackBasic)EyeCallback));
            eye_callback_registered = false;
        }

        Ray gazeRay;
        bool eye_focus = false;
        FocusInfo focusInfo = new FocusInfo();
        int stimulusLayerId = LayerMask.NameToLayer("stimulusToTrack");
        LayerMask layerMask = 1 << stimulusLayerId;

        GazeIndex gazeIndex = GazeIndex.COMBINE;

        if (eye_callback_registered)
        {

            eye_focus = SRanipal_Eye.Focus(gazeIndex, out gazeRay, out focusInfo, 0, MaxDistance, layerMask, eyeData);
        }
        else
        {

            eye_focus = SRanipal_Eye.Focus(gazeIndex, out gazeRay, out focusInfo, 0, MaxDistance, layerMask);
        }
        looking_at_stim = false;
        if (StimulusObject != null && focusInfo.transform != null && eye_focus)
        {
            looking_at_stim = (focusInfo.transform.gameObject == StimulusObject);
            HighlightObject(eye_focus && focusInfo.transform.gameObject == StimulusObject);
        }
        else
        {
            HighlightObject(false);
        }

        if (eye_focus)
        {
            Vector3 localFocusPoint = StimulusObject.transform.InverseTransformPoint(focusInfo.point);
            float actualTime = Time.time - startTime;
            outputStream.WriteLine($"{actualTime},{localFocusPoint.x},{localFocusPoint.y},{looking_at_stim.ToString()}");
        }
    }

    void HighlightObject(bool highlight)
    {
        centralStimulus centralStimulus = StimulusObject.GetComponent<centralStimulus>();
        if (centralStimulus != null)
        {
            centralStimulus.Highlight(highlight);
        }
    }

    public bool IsLookingAtStimulus()
    {
        return looking_at_stim;
    }


    private void OnApplicationQuit()
    {
        if (outputStream != null)
        {
            outputStream.Close();
        }
    }

    private static void EyeCallback(ref EyeData eye_data)
    {
        eyeData = eye_data;
    }

    public void StopTracking()
    {
        if (outputStream != null)
        {
            outputStream.Close();
            outputStream = null;
        }

        centralStimulus centralStimulus = StimulusObject.GetComponent<centralStimulus>();
        if (centralStimulus != null)
        {
            centralStimulus.Finished();
        }

        this.enabled = false;
    }

}