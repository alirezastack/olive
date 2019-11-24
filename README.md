Olive is a module to have shared resources in one place. Some core methods like RPCClient, GRPCServer methods reside here.

# Olive Structure
 - proto
   - rpc
   - zoodroom.proto
   - zoodroom_pb2
   - zoodroom_pb2_grpc
 - store
   - mongo_connection
 - authentication
 - consts
 - exc
 - patterns
 - toolbox
 - validation


# Installation:
For installation of Olive, below link is added to requirements.txt of the service:

```
-e git+https://oauth2:YOUR_OAUTH_TOKEN@git.YOUR_REPO.com/basket/olive.git@master#egg=olive
```

# Definition:
proto folder house anything related to gRPC (proto file, pb files, RPC client and RPC server).

The store folder contains anything that is related to database connection or models which is common across services. 

consts file includes all constants like date format that is consistent for all datetime fields.

exc: if you have a new exception class that is used in you module put it here, it may be used by other services too.

patterns: design patterns used by services like singleton, factory and so on.

toolbox: handy methods which is something similar to a utility will be put here.

validation: any method related to validation is here like is_url_valid.



Shared libraries between modules like pymongo, marshmallow, etc are inside of requirements.txt which will be installed as dependency of Olive library.


### Warning:
If you make a change in the library make sure to increase the versioning in setup.py file before the push. If it is minor bug fix increase the 3rd number if it has backward incompatible change increase the major version and so on.


### Info:
Any new library that is common between services should be put both in requirements.txt of service itself and Olive too

