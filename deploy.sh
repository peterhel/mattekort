BUCKET_NAME=$1
DISTRIBUTION_ID=$2
aws s3 sync --exclude '.git/*' --exclude deploy.sh . "s3://$BUCKET_NAME"
aws s3api put-object-acl --bucket $BUCKET_NAME --key index.html --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key stora.html --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key handskrift.html --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key thumb.webp --acl public-read
aws s3api put-object-acl --bucket $BUCKET_NAME --key poop.gif --acl public-read

aws s3 website "s3://$BUCKET_NAME" --index-document index.html
echo "http://$BUCKET_NAME.s3-website.eu-north-1.amazonaws.com/"

aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/index.html" "/handskrift.html" "/stora.html"

pushd mattekort-textract
rm function.zip || true
zip function.zip lambda_function.py
AWS_DEFAULT_REGION=us-east-1 aws lambda update-function-code --function-name mattekort-textract --zip-file fileb://function.zip | cat
popd