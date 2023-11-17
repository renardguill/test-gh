using System.Text.Json;

private class Cluster {
    public string ClusterName { get; set; }
    public string ManifestPath { get; set; }
}


var clusters = new List<Cluster>();
clusters.Add(new Cluster { ClusterName = "cluster-1", ManifestPath = "cluster-1.yaml" });
clusters.Add(new Cluster { ClusterName = "cluster-2", ManifestPath = "cluster-2.yaml" });
clusters.Add(new Cluster { ClusterName = "cluster-3", ManifestPath = "cluster-3.yaml" });

var clustersMatrix = new Dictionary<string, List<Cluster>> {
    { "include", clusters }
};

Task("default").Does(() =>
{
    if (BuildSystem.IsRunningOnGitHubActions)
    {
        Information("Running on GitHub Actions");

        var clustersMatrixString = JsonSerializer.Serialize(clustersMatrix);
        Information($"Cluster matrix: {clustersMatrixString}");
        BuildSystem.GitHubActions.Commands.SetOutputParameter("clusters-matrix", clustersMatrixString);
        BuildSystem.GitHubActions.Commands.SetSecret("testSecret");
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
            Information($"{cluster.ClusterName} => {cluster.ManifestPath}");
        }
    }
});


RunTarget("default");