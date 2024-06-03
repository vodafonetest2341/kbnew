Create PROC [knowledgebase].[RemoveDocument](
    @container varchar(1000),
    @directory varchar(1000),
    @filePath varchar(1000)
)
AS
    Delete from knowledgebase.Document where Destination = @container+'/'+@directory+'/'+@filePath

GO

