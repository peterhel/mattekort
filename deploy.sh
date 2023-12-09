BUCKET_NAME=$1
aws s3 sync --exclude '.git/*' --exclude deploy.sh . "s3://$BUCKET_NAME"
aws s3api put-object-acl --bucket $BUCKET_NAME --key index.html --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key thumb.webp --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key poop.gif --acl public-read

aws s3 website "s3://$BUCKET_NAME" --index-document index.html
echo "http://$BUCKET_NAME.s3-website.eu-north-1.amazonaws.com/"