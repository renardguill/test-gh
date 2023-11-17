using System.Text.Json;

private class Cluster {
    public string Name { get; set; }
    public string ManifestPath { get; set; }
}


var clusters = new List<Cluster>();
clusters.Add(new Cluster { Name = "cluster-1", ManifestPath = "cluster-1.yaml" });
clusters.Add(new Cluster { Name = "cluster-2", ManifestPath = "cluster-2.yaml" });
clusters.Add(new Cluster { Name = "cluster-3", ManifestPath = "cluster-3.yaml" });

var clusterMatrix = new Dictionary<string, List<Cluster>> {
    { "include", clusters }
};

Task("default").Does(() =>
{
    if (BuildSystem.IsRunningOnGitHubActions)
    {
        Information("Running on GitHub Actions");

        var clusterMatrixString = JsonSerializer.Serialize(clusterMatrix);
        Information($"Cluster matrix: {clusterMatrixString}");
        BuildSystem.GitHubActions.Commands.SetOutputParameter("clusters-matrix", clusterMatrixString);
        Information($"Workflow Ref: {BuildSystem.GitHubActions.Environment.Workflow.Ref}");
        Information($"Workflow RefName: {BuildSystem.GitHubActions.Environment.Workflow.RefName}");
        Information($"Workflow RefType: {BuildSystem.GitHubActions.Environment.Workflow.RefType}");
        Information($"Workflow IsPullRequest: {BuildSystem.IsPullRequest}");
        Information($"Workflow BaseRef: {BuildSystem.GitHubActions.Environment.Workflow.BaseRef}");
        Information($"Workflow Workspace: {BuildSystem.GitHubActions.Environment.Workflow.Workspace}");
        
    }
    else
    {
        Information("Running locally");
        Information("Cluster matrix:");
        foreach (var cluster in clusters)
        {
            Information($"{cluster.Name} => {cluster.ManifestPath}");
        }
    }
});


RunTarget("default");