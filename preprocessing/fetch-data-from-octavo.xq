import module namespace functx = 'http://www.functx.com';
declare namespace output = "http://www.w3.org/2010/xslt-xquery-serialization";
declare option output:method "csv";
declare option output:csv "header=yes, separator=|";

(: XQuery script for fetching data from Octavo API using lemmatized keywords.:)
(: To be used with BaseX <http://basex.org> :)

 
 
 
(: Lemmatize search string to a format suitable for 
   lemmatized index :)
 
declare function local:lemmatize($word as xs:string) as xs:string* {
  let $url:="http://demo.seco.tkk.fi/las/baseform?text="||encode-for-uri($word) ||"&amp;maxEditDistance=0&amp;depth=1"
  let $data :=  
  try {http:send-request(
  <http:request method='get'
     override-media-type='text/plain'
     href='{$url}' timeout='160' >
  </http:request>
)[2]} catch * {}
  
  return if (string-length($data) > 3) then
      $data
      else ('{"baseform":"NA"}')  
};


(: Create querystring from a keyword :)

declare function local:create-bl-query($word) {
      
      let $lemmatized:=
      normalize-space(
        json:parse(local:lemmatize($word))//baseform)
      
      let $lemmatized_query_parts:=tokenize($lemmatized)
  
  return  '"' || string-join(
    for $lemma in $lemmatized_query_parts
     return 'BL=' || $lemma, ' ') || '"'
  
};

declare function local:create-keyword-list($search_subjects) as node()* {
  
  let $keywords:=
    switch($search_subjects)
      case 'political-agents' return db:open("keywords","keywords-political_agents.csv")/csv/record/keyword
      case 'electoral-districts' return db:open("keywords",'keywords-parliament-members.csv')/csv/record/piiri
      case 'parliament-members' return for $person in db:open("keywords-parliament_members.csv")/csv/record
                                        return $person/etunimi || ' ' || $person/sukunimi
      case 'areas' return  db:open("keywords","keywords-areas.csv")/text/line
      case 'equality' return db:open("keywords","keywords-equality.txt")/text/line
      case 'energy' return db:open("keywords","keywords-nergy.txt")/text/line
      case "migration-extra" return db:open("keywords","keywords-migration-special-interest.txt")/text/line
    default return <line>ERROR</line>
    
  return $keywords

  
  
};




(: Main function for fectching data from Octavo API :)
(: Make sure to set the output directory for file:write -function in line 120 ! :)

for $keyword in local:create-keyword-list('migration-extra')
  (: Rate limit 1 query per 3 seconds :)
  let $wait:=prof:sleep(3000)
  let $querystring:= local:create-bl-query($keyword)
  let $url:="https://vm0824.kaj.pouta.csc.fi/octavo/hs-migration/search?query="||encode-for-uri("<ARTICLE§" || $querystring || "§ARTICLE>")||"&amp;pretty&amp;field=articleID&amp;field=timePublished&amp;limit=-1&amp;timeout=160"

  (: Call Octavo API :)

  let $results :=  
    try {json:parse(http:send-request(
      <http:request method='get'
        override-media-type='text/plain'
        href='{$url}' timeout='160' >
      </http:request>
    )[2])} catch * {}

  let $entries:= 

    if (count($results/json/results/docs/_)>1) then
  
      for $result in $results/json/results/docs/_
        let $hits:=$results/../../total
        let $article_id :=$result/articleID
        let $timepublished:=$result/timePublished        
        
        return
        <entry>
          <query>{$querystring}</query>
          <keyword>{data($keyword)}</keyword>
          <timestamp>{data($result/timePublished)}</timestamp>
          <article_id>{data($article_id)}</article_id>
        </entry>
    else(
        <entry>
          <query>{$querystring}</query>
          <keyword>{data($keyword)}</keyword>
          <timestamp>NA</timestamp>
          <article_id>NA</article_id>
        </entry>
        )
     
    
 let $csv:=
 <csv>
  {$entries}
 </csv>
   
return file:write('/YOUR_OUTPUT_DIRECTORY/'||random:uuid()||'.csv',csv:serialize($csv))

