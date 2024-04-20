// Initiate config replica set mongosh
rs.initiate({
  _id: "config_rs",
  configsvr: true,
  members: [
    { _id: 0, host: "host.docker.internal:10001" },
    { _id: 1, host: "host.docker.internal:10002" },
    { _id: 2, host: "host.docker.internal:10003" }
  ]
})

// Initiate shard replica set
rs.initiate(
  {
    _id : "shard1_rs",
    members: [
      { _id : 0, host : "host.docker.internal:10101" },
      { _id : 1, host : "host.docker.internal:10102" },
      { _id : 2, host : "host.docker.internal:10103" },
    ]
  }
)

// Add shards to mongos
sh.addShard( "shard1_rs/host.docker.internal:10101,host.docker.internal:10102,host.docker.internal:10103")

// Add shard to replica set

rs.add( { host: "host.docker.internal:27018" } )


rs.initiate(
  {
    _id : "shard2_rs",
    members: [
      { _id : 0, host : "host.docker.internal:27018" }
    ]
  }
)

sh.addShard( "shard2_rs/host.docker.internal:27018")