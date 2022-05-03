const getQueryParams = () => {
  const params = new URLSearchParams(window.location.search);
  let name = params.get("name");
  let age = params.get("age");
  let s1 = params.get("s1");
  let s2 = params.get("s2");
  let s3 = params.get("s3");
  let id = params.get("id");
  return {
    name: name,
    age: age,
    s1: s1,
    s2: s2,
    s3: s3,
    id: id,
  };
};
const generateQueryString = () => {
  const params = getQueryParams();
  return `?name=${params.name}&age=${params.age}`;
};
