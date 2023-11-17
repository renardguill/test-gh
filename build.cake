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
    if (BuildSystem.IsRunningOnGitHubActions)
    {
        Information("Running on GitHub Actions");
        BuildSystem.GitHubActions.Commands.SetOutputParameter("matrix", JsonSerializer.Serialize(clusterMatrix));
        Information($"Workflow Ref: {BuildSystem.GitHubActions.Environment.Workflow.Ref}");
        Information($"Workflow RefName: {BuildSystem.GitHubActions.Environment.Workflow.RefName}");
        Information($"Workflow RefType: {BuildSystem.GitHubActions.Environment.Workflow.RefType}");
        Information($"Workflow BaseRef: {BuildSystem.GitHubActions.Environment.Workflow.BaseRef}");
        Information($"Workflow BaseRef: {BuildSystem.GitHubActions.Environment.Workflow.Workspace}");
        
    }
    else
    {
        Information("Running locally");
        Information("Cluster matrix:");
        foreach (var cluster in clusterMatrix["include"])
        {
            Information($"  {cluster["cluster"]}");
        }
    }
});


RunTarget("default");