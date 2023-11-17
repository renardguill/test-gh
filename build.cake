using System.Text.Json;

var clusterMatrix = new Dictionary<string, Dictionary<string, string>[]>
{
    { 
        "include", new []
        {
            new Dictionary<string, string> { { "cluster", "cluster-1" }},
            new Dictionary<string, string> { { "cluster", "cluster-2" }},
            new Dictionary<string, string> { { "cluster", "cluster-3" }},
        }
    },
};

Task("default").Does(() =>
{
    BuildSystem.GitHubActions.Commands.SetOutputParameter("matrix", JsonSerializer.Serialize(clusterMatrix));
});


RunTarget("default");