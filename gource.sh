for repo in $(ls workdir)
do
   cd workdir/$repo
   git log --pretty=format:user:%aN%n%ct\
      --reverse\
      --raw --encoding=UTF-8\
      --no-renames -40 > /tmp/gitlog

   gource -600x480\
      -s 2\
      -e 0.3\
      -r 30\
      -a 1 -o - \
      --log-format git --stop-at-end /tmp/gitlog \
      \
      | avconv -y -r 60 -f image2pipe -vcodec ppm -i -\
      -vcodec libx264 -preset ultrafast -pix_fmt yuv420p\
      -crf 1 -threads 0 -bf 0 ../../django/hub/static/hub/$repo.mp4
   cd -
done; 
