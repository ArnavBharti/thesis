-- Keep long identifiers readable without changing the Markdown/raw evidence.
local function tex_escape(text)
  local map = {['\\']='\\textbackslash{}', ['{']='\\{', ['}']='\\}', ['%']='\\%', ['&']='\\&', ['#']='\\#', ['$']='\\$', ['_']='\\_', ['~']='\\textasciitilde{}', ['^']='\\textasciicircum{}'}
  return (text:gsub('[\\{}%%&#$_~^]', map))
end

function Code(element)
  local parts = {}
  -- ASCII separators only: locale-sensitive %S can split UTF-8 dagger bytes.
  for word in element.text:gmatch('[^ \t\r\n]+') do
    table.insert(parts, '\\seqsplit{' .. tex_escape(word) .. '}')
  end
  return pandoc.RawInline('latex', '\\texttt{' .. table.concat(parts, '\\ ') .. '}')
end

function Str(element)
  if element.text:find('_') then
    local parts = {}
    local first = true
    for part in element.text:gmatch('[^_]+') do
      if not first then
        table.insert(parts, pandoc.RawInline('latex', '\\_\\allowbreak '))
      end
      table.insert(parts, pandoc.Str(part))
      first = false
    end
    return parts
  end
end
