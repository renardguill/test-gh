using System.Text.Json;

private class Cluster {
    public string ClusterName { get; set; }
    public string ManifestPath { get; set; }
}


var clusters = new List<Cluster>();
clusters.Add(new Cluster { ClusterName = "cluster-4", ManifestPath = "cluster-4.yaml" });
clusters.Add(new Cluster { ClusterName = "cluster-5", ManifestPath = "cluster-5.yaml" });
clusters.Add(new Cluster { ClusterName = "cluster-6", ManifestPath = "cluster-6.yaml" });



Task("default").Does(() =>
{
    if (BuildSystem.IsRunningOnGitHubActions)
    {
        Information("Running on GitHub Actions");

        if (BuildSystem.IsPullRequest)
        {
            clusters.Add(new Cluster { ClusterName = "cluster-6_" + BuildSystem.GitHubActions.Environment.Workflow.RunId, ManifestPath = "cluster-6.yaml" });
            clusters.Add(new Cluster { ClusterName = "cluster-6_" + BuildSystem.GitHubActions.Environment.Workflow.RunId, ManifestPath = "cluster-6-n+1.yaml" });
            BuildSystem.GitHubActions.Commands.SetOutputParameter("max-parallel", "1");
        } else {
            BuildSystem.GitHubActions.Commands.SetOutputParameter("max-parallel", "3");
        }

        var clustersMatrix = new Dictionary<string, List<Cluster>> {
            { "include", clusters }
        };

        Information("GitHub Output:");
        Information(EnvironmentVariable("GITHUB_OUTPUT"));
        var clustersMatrixString = JsonSerializer.Serialize(clustersMatrix);
        Information($"Cluster matrix: {clustersMatrixString}");
        BuildSystem.GitHubActions.Commands.SetOutputParameter("clusters-matrix", clustersMatrixString);
        Information("GitHub Output:");
        Information(EnvironmentVariable("GITHUB_OUTPUT"));
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