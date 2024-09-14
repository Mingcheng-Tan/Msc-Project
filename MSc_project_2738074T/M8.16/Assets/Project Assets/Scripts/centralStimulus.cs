using UnityEngine;

public class centralStimulus : MonoBehaviour
{
    public Material idleMaterial; // passes in the idle colour of the central point
    private Renderer renderer;

    void Start()
    {
        renderer = GetComponent<Renderer>();
    }

    void Update()
    {
    }

    public void SetColor(Color color) 
    {
        if (renderer != null)
        {
            MaterialPropertyBlock propBlock = new MaterialPropertyBlock(); // creates a material block, they are good for high speed rendering, for instance if an object is changing colour often
            renderer.GetPropertyBlock(propBlock);
            propBlock.SetColor("_Color", color);
            renderer.SetPropertyBlock(propBlock);
        }
    }


    public void Highlight(bool isFocused) // used to change colour of centre point, true boolean will set colour to green
    {
        SetColor(isFocused ? Color.green : Color.red);
    }

    public void Finished() // finished method is used to set centre to an idle orange colour
    {
    if (renderer != null && idleMaterial != null)
    {

        renderer.SetPropertyBlock(null);
        renderer.material = idleMaterial;
    }
    }
}
