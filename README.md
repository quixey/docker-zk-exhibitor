Forked from https://github.com/quixey/docker-zk-exhibitor

### Versions
* Exhibitor 1.5.5
* ZooKeeper 3.4.6

### Usage

Building the container: 

    ./build_image.sh
   
Starting the container:

    ./run_image.sh 

Once the container is up, confirm Exhibitor is running:

    $ curl -s localhost:8181/exhibitor/v1/cluster/status | python -m json.tool
    [
        {
            "code": 3, 
            "description": "serving", 
            "hostname": "<host>", 
            "isLeader": true
        }
    ]
_See Exhibitor's [wiki](https://github.com/Netflix/exhibitor/wiki/REST-Introduction) for more details on its REST API._

You can also check Exhibitor's web UI at `http://<host>:8181/exhibitor/v1/ui/index.html`

Then confirm ZK is available:

    $ echo ruok | nc <host> 2181
    imok

### AWS IAM Policy
Exhibitor can also use an IAM Role attached to an instance instead of passing access or secret keys. This is an example policy that would be needed for the instance:
```
{
    "Statement": [
        {
            "Resource": [
                "arn:aws:s3:::exhibitor-bucket/*",
                "arn:aws:s3:::exhibitor-bucket"
            ],
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:GetBucketAcl",
                "s3:GetBucketPolicy",
                "s3:GetObject",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
                "s3:ListMultipartUploadParts",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Effect": "Allow"
        }
    ]
}
```

