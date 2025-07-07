using UnityEngine;
using Newtonsoft.Json;
using System.Collections.Generic;

public class WaypointSpawner : MonoBehaviour
{
    [Header("Inputs")]
    public TextAsset jsonFile;                  // Your waypoints_detected.json file
    public GameObject defaultWaypointPrefab;    // The sphere or icon you want to spawn

    [Header("Map Dimensions")]
    public float imageWidth = 2036f;            // Actual pixel width of map image
    public float imageHeight = 1527f;           // Actual pixel height of map image
    public float worldWidth = 10f;              // Width of plane in Unity units
    public float worldHeight = 13f;             // Height of plane in Unity units

    void Start()
    {
        var allPoints = JsonConvert.DeserializeObject<Dictionary<string, List<IconPoint>>>(jsonFile.text);

        foreach (var entry in allPoints)
        {
            string category = entry.Key;

            foreach (var point in entry.Value)
            {
                // Normalize image-space coordinates (0–1)
                float normalizedX = point.x / imageWidth;
                float normalizedY = point.y / imageHeight;

                // Map to Unity world space (flipping Y to Z)
                float x = normalizedX * worldWidth;
                float z = (1f - normalizedY) * worldHeight;

                Vector3 worldPos = new Vector3(x, 0f, z);

                GameObject marker = Instantiate(defaultWaypointPrefab, worldPos, Quaternion.identity, this.transform);
                marker.name = $"{category}_Waypoint";
            }
        }
    }
}

[System.Serializable]
public class IconPoint
{
    public int x;
    public int y;
}
