while true
do

echo $(which cur)

TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
echo $TOKEN
ANS=`curl -H "X-aws-ec2-metadata-token: $TOKEN" -v "http://169.254.169.254/latest/meta-data/ami-id"`
echo $ANS
aws s3api list-buckets
  # loop infinitely
done