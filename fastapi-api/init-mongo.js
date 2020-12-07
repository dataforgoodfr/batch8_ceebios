print('Start #################################################################');

db = db.getSiblingDB('ceebios');
db.createUser({
  user: "ceebiosAdmin",
  pwd: "vespaducalis",
  roles: [
    {
      role: "readWrite",
      db: "ceebios",
    },
  ]
});
